#!/usr/bin/env python

import os
import yaml
from src.orchestrator import FactCheckOrchestrator

if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    with open("sample_text.txt", "r") as f:
        sample_text = f.read().strip()

    print(f"Running verification on sample text:\n\n{sample_text}\n\n")

    orchestrator = FactCheckOrchestrator(config)
    print(orchestrator.verify(sample_text))