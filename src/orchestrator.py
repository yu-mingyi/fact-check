#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import importlib
import os
from typing import TypedDict, List

# Libs
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END

# Custom


##################
# Configurations #
##################

# Mappings
from .mappings import SOURCE_MAPPING, API_MAPPING

# Prompts
from .prompts import ANALYST_PROMPT, VERIFIER_PROMPT, SUMMARIZER_PROMPT, REVISER_PROMPT

# Pydantic Models 
from .pydantic_models import Claim, Claims, Evaluation, Summary


###########
# Classes #
###########

class AgentState(TypedDict):
    input_text: str
    claims: List[Claim]
    evaluations: List[Evaluation]
    summary: str
    needs_revision: bool
    revised_text: str

class FactCheckOrchestrator:
    def __init__(self, config):
        self._agent_config = config["agent_config"]
        self._llm = self._load_llm(config["llm"])
        self._sources = {
            source["config"]["id"]: self._load_source(source) 
            for source 
            in config["sources"]
        }
        self._graph = self._build_graph()
        self._thread = {"configurable": {"thread_id": "1"}}


    def verify(self, input_text):
        final_state = self._graph.invoke(
            {"input_text": input_text}, 
            config = self._thread
        )
        print(final_state)
        return final_state


    # Nodes
    def analyst_node(self, state: AgentState):
        sources = "\n".join([
            f"{source_id} -> {source.description}" 
            for source_id, source 
            in self._sources.items()
        ])
        print("Beginning analysis...")
        claims = self._llm.with_structured_output(Claims).invoke([
            HumanMessage(content=ANALYST_PROMPT.format(
                sources=sources, 
                input_text=state["input_text"]
            ))
        ])
        print("Analysis completed. Claims found:", claims)
        return {"claims": claims.claims}

    def verifier_node(self, state: AgentState):
        MAX_CHECKS = self._agent_config["max_checks"]
        evaluations = []
        structured_llm = self._llm.with_structured_output(Evaluation)
        for claim in state["claims"][:MAX_CHECKS]:
            responses = []
            for source in claim.sources:
                try: 
                    responses = self._sources[source].query(claim.claim)
                    responses.extend(responses)
                except Exception as e:
                    print(f"Error querying source {source}: {e}")
            statements = ", ".join([
                f"[{r['title']}, {source}] -> {r['text']}" 
                for r 
                in responses
            ])
            print("Beginning evaluation of claim:\n", claim.claim, "\nagainst statements:\n", statements)
            evaluation = structured_llm.invoke([
                HumanMessage(content=VERIFIER_PROMPT.format(
                    claim=claim.claim, 
                    statements=statements
                ))
            ])
            print("Evaluation completed:\n", evaluation)
            evaluations.append(evaluation)
        return {"evaluations": evaluations}

    def summarizer_node(self, state: AgentState):
        evidence = "\n\n".join([
            f"- Evaluation: {e.evaluation}\n- Conflict: {e.conflict}"
            for e 
            in state["evaluations"]
        ])
        print("Beginning summary ...")
        summary = self._llm.with_structured_output(Summary).invoke([
            HumanMessage(content=SUMMARIZER_PROMPT.format(evidence=evidence))
        ])
        print("Summary completed:\n", summary)
        return {
            "summary": summary.summary, 
            "needs_revision": summary.needs_revision
        }

    def reviser_node(self, state: AgentState):
        print("Beginning revision ...")
        response = self._llm.invoke([
            HumanMessage(content=REVISER_PROMPT.format(
                input_text=state["input_text"], 
                feedback=state["summary"]
            ))
        ])
        print("Revision completed:\n", response.content)
        return {"revised_text": response.content}

    def needs_revision(self, state: AgentState) -> str:
        return "reviser" if state["needs_revision"] else END


    # Helpers
    def _load_llm(self, llm_config):
        print("Loading LLM ...")
        try:
            api_env_var = API_MAPPING[llm_config["load_params"]["module"]]
            if api_env_var not in os.environ:
                os.environ[api_env_var] = llm_config["load_params"]["api_key"]
            return getattr(
                importlib.import_module(llm_config["load_params"]["module"]), 
                llm_config["load_params"]["class"]
            )(**llm_config["init_params"])
        except Exception as e:
            raise(f"Error loading LLM: {e}")

    def _load_source(self, source):
        print(f"Loading source '{source['config']['id']}'...")
        try:
            source_module, source_class = SOURCE_MAPPING[source["source_type"]]
            return getattr(
                importlib.import_module(f"src.sources.{source_module}"), 
                source_class
            )(source["config"])
        except Exception as e:
            raise(f"Error loading source: {e}")

    def _build_graph(self):
        builder = StateGraph(AgentState)

        nodes = [            
            ("analyst", self.analyst_node),
            ("verifier", self.verifier_node),
            ("summarizer", self.summarizer_node),
            ("reviser", self.reviser_node)
        ]

        edges = [
            ("analyst", "verifier"),
            ("verifier", "summarizer"),
            ("reviser", END)
        ]

        for node_name, node_fn in nodes:
            builder.add_node(node_name, node_fn)

        builder.set_entry_point("analyst")
        builder.add_conditional_edges(
            "summarizer", 
            self.needs_revision,
            {"reviser": "reviser", END: END}
        )

        for from_node, to_node in edges:
            builder.add_edge(from_node, to_node)

        return builder.compile()
