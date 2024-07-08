import os
import pkgutil

package_dir = os.path.dirname(__file__)

for _, module_name, _ in pkgutil.iter_modules([package_dir]):
    __import__(f'{__name__}.{module_name}')