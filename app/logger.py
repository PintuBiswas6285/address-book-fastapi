# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
import logging

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)