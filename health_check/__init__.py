"""health-check: lightweight Healthchecks.io ping client."""

from health_check._config import load_config
from health_check._ping import ping, ping_fail

__version__ = "1.0.2"
__all__ = ["ping", "ping_fail", "load_config"]
