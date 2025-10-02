# src/utils/env.py
import os
import yaml
import re
from pathlib import Path
from dotenv import load_dotenv

def load():
    """
    Load config.yaml with .env variable expansion.
    Example: ${VT_API_KEY} will be replaced with actual value from .env
    """
    # Load .env file into environment
    load_dotenv()

    cfg_file = Path("config/config.yaml")  # <-- updated path
    if not cfg_file.exists():
        raise FileNotFoundError("config/config.yaml not found")

    # Read raw YAML text
    with open(cfg_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Replace ${VAR} with environment variables
    def replace_env_var(match):
        var_name = match.group(1)
        return os.getenv(var_name, match.group(0))  # fallback = leave as-is

    expanded = re.sub(r"\$\{([^}]+)\}", replace_env_var, text)

    return yaml.safe_load(expanded)

def getenv(key, default=None):
    """
    Get an environment variable, or return default if not set.
    """
    return os.getenv(key, default)


