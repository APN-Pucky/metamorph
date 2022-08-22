from .handler import generate_alternatives, translate
from .config import Config

import pkg_resources as pkg  # part of setuptools

package = "metamorph"

try:
    version = pkg.require(package)[0].version
except pkg.DistributionNotFound:
    version = "dirty"