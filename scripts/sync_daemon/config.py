"""Configuration loader for DOKODU BRAIN ↔ CRM Sync Daemon.

Reads from ~/.config/dokodu/sync_config.json with built-in defaults.
API key resolved from file or CRM_API_KEY environment variable.
"""

import json
import os
from pathlib import Path


DEFAULTS = {
    "brain_repo_path": "/srv/dokodu-brain",
    "crm_base_url": "https://system.dokodu.it",
    "crm_api_key_file": "~/.config/dokodu/crm_api_key",
    "sync_interval_seconds": 300,
    "state_file": ".sync_state.json",
    "mapping_file": ".sync_mapping.json",
    "lock_file": "/tmp/dokodu-sync.lock",
    "log_dir": "/var/log/dokodu-sync",
}

CONFIG_PATH = Path("~/.config/dokodu/sync_config.json").expanduser()


def load_config() -> dict:
    """Load configuration from file, falling back to defaults.

    Returns a dict with all config keys resolved (paths expanded).
    """
    config = dict(DEFAULTS)

    if CONFIG_PATH.exists():
        try:
            with CONFIG_PATH.open("r", encoding="utf-8") as f:
                overrides = json.load(f)
            config.update(overrides)
        except (json.JSONDecodeError, OSError) as exc:
            # Non-fatal: log and use defaults
            import logging
            logging.getLogger(__name__).warning(
                "Failed to read %s: %s — using defaults", CONFIG_PATH, exc
            )

    # Expand ~ in path-like values
    for key in ("brain_repo_path", "crm_api_key_file", "log_dir"):
        if key in config and isinstance(config[key], str):
            config[key] = str(Path(config[key]).expanduser())

    # Resolve CRM API key
    config["crm_api_key"] = _resolve_api_key(config.get("crm_api_key_file", ""))

    return config


def _resolve_api_key(key_file_path: str) -> str:
    """Return API key from environment variable or key file.

    Precedence: CRM_API_KEY env var > file at key_file_path.
    Returns empty string if neither is available.
    """
    env_key = os.environ.get("CRM_API_KEY", "").strip()
    if env_key:
        return env_key

    if key_file_path:
        path = Path(key_file_path).expanduser()
        if path.exists():
            try:
                return path.read_text(encoding="utf-8").strip()
            except OSError:
                pass

    return ""
