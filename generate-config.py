#!/usr/bin/env python3
"""Generate Hermes config.yaml with models from Vultr Inference API.

Fetches /v1/models, excludes safety/guard models, and writes config.yaml.
Usage: python3 generate-config.py <API_KEY>
"""
import json
import sys
import urllib.request

# Models to exclude — safety/guard models, not chat models
EXCLUDED_MODELS = {
    "nvidia/Nemotron-3.5-Content-Safety",
    "nvidia/Llama-3.1-Nemotron-Safety-Guard-8B-v3",
}

BASE_URL = "https://api.vultrinference.com/v1"
DEFAULT_MODEL = "zai-org/GLM-5.1-FP8"
FALLBACK_MODELS = {
    "zai-org/GLM-5.1-FP8": {"context_window": 202752, "max_tokens": 8192},
}


def fetch_models(api_key: str) -> dict:
    """Fetch models from /v1/models, returning {id: {context_window, max_tokens}}."""
    req = urllib.request.Request(
        f"{BASE_URL}/models",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"Warning: Failed to fetch models: {e}", file=sys.stderr)
        return FALLBACK_MODELS

    models = {}
    for m in data.get("data", []):
        mid = m.get("id", "")
        if not mid or mid in EXCLUDED_MODELS:
            continue
        ctx = m.get("max_model_len", 128000)
        models[mid] = {"context_window": ctx, "max_tokens": 8192}

    if not models:
        print("Warning: No models found, using fallback", file=sys.stderr)
        return FALLBACK_MODELS

    return models


def generate_config(api_key: str, models: dict) -> str:
    """Generate the config.yaml content."""
    # Build models YAML block (6-space indent to nest under providers.vultr)
    models_yaml = ""
    for mid, info in models.items():
        models_yaml += f"      {mid}:\n"
        models_yaml += f"        context_window: {info['context_window']}\n"
        models_yaml += f"        max_tokens: {info['max_tokens']}\n"

    return f"""model:
  provider: "custom"
  default: "{DEFAULT_MODEL}"
  base_url: "{BASE_URL}"
  api_key: "{api_key}"
  api_mode: "chat_completions"

providers:
  vultr:
    base_url: "{BASE_URL}"
    api_key: "{api_key}"
    auth: "token"
    api_mode: "chat_completions"
    discover_models: false
    models:
{models_yaml}
auxiliary:
  compression:
    provider: "vultr"
    model: "nvidia/DeepSeek-V3.2-NVFP4"
    base_url: "{BASE_URL}"
    api_key: "{api_key}"
    timeout: 120

terminal:
  backend: "local"
  cwd: "/home/hermes"
  timeout: 180

display:
  tool_progress: "new"

memory:
  enabled: true

skills:
  enabled: true

cron:
  enabled: true
"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate-config.py <API_KEY>", file=sys.stderr)
        sys.exit(1)

    api_key = sys.argv[1]
    models = fetch_models(api_key)
    config = generate_config(api_key, models)

    with open("/home/hermes/.hermes/config.yaml", "w") as f:
        f.write(config)

    print(f"Config written with {len(models)} models: {', '.join(models.keys())}")


if __name__ == "__main__":
    main()
