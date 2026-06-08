import os
from pathlib import Path


def load_config(config_file: Path | None = None) -> dict:
    """Load configuration from file, falling back to environment variables."""
    path = config_file or Path.home() / ".config" / "health-check"
    config = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()

    config.setdefault("HEALTHCHECK_URL", os.environ.get("HEALTHCHECK_URL", ""))
    config.setdefault("DEVICE_NAME", os.environ.get("DEVICE_NAME", "unknown"))
    return config
