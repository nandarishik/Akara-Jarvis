from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"missing model config: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"invalid YAML root in {path}")
    return data


class ModelRegistry:
    def __init__(self, config_dir: Path) -> None:
        self.config_dir = config_dir
        self.raw = _load_yaml(config_dir / "model-registry.yaml")
        self.models: dict[str, Any] = dict(self.raw.get("models") or {})

    def get_model(self, key: str) -> dict[str, Any]:
        if key not in self.models:
            raise KeyError(f"unknown model key: {key}")
        return self.models[key]

    def provider_entry(self, model_key: str, provider: str) -> dict[str, Any] | None:
        model = self.get_model(model_key)
        providers = model.get("providers") or {}
        entry = providers.get(provider)
        return entry if isinstance(entry, dict) else None
