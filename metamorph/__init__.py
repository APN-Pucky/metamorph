from .config import Config
from .handler import generate_alternatives, translate

__all__ = ["generate_alternatives", "translate", "Config"]

from importlib.metadata import version

package = "metamorph"

__version__ = version(package)
