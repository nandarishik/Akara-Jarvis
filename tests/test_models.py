from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from jarvis.models.providers import any_provider_key, api_key_for
from jarvis.models.registry import ModelRegistry
from jarvis.models.router import ModelRouter
from jarvis.models.routing import ModelRouting, ProviderFallbacks

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"


@pytest.fixture
def settings_or_only():
    return SimpleNamespace(
        openrouter_api_key="sk-or-test",
        deepseek_api_key="",
        minimax_api_key="",
        zai_api_key="",
        moonshot_api_key="",
        mistral_api_key="",
        groq_api_key="",
        deepinfra_api_key="",
        fireworks_api_key="",
        cerebras_api_key="",
        daily_spend_cap_usd=50.0,
        model_config_dir=str(CONFIG),
    )


def test_yaml_loads():
    reg = ModelRegistry(CONFIG)
    assert "minimax_m3" in reg.models
    routing = ModelRouting(CONFIG)
    assert "backend_agent" in routing.agents
    fb = ProviderFallbacks(CONFIG)
    assert "minimax_m3_chain" in fb.chains


def test_backend_alias_and_openrouter_when_only_or(settings_or_only):
    router = ModelRouter(settings_or_only, conn=None)
    router.config_dir = CONFIG
    router.registry = ModelRegistry(CONFIG)
    router.routing = ModelRouting(CONFIG)
    router.fallbacks = ProviderFallbacks(CONFIG)

    resolved = router.resolve("backend")
    assert resolved.model_key == "minimax_m3"
    assert resolved.provider == "openrouter"
    assert "minimax" in resolved.model_id.lower()

    model_str, key = router.openhands_model("backend")
    assert model_str.startswith("openrouter/")
    assert key == "sk-or-test"


def test_high_risk_backend_escalates(settings_or_only):
    router = ModelRouter(settings_or_only, conn=None)
    router.config_dir = CONFIG
    router.registry = ModelRegistry(CONFIG)
    router.routing = ModelRouting(CONFIG)
    router.fallbacks = ProviderFallbacks(CONFIG)

    resolved = router.resolve("backend", high_risk=True)
    assert resolved.model_key == "deepseek_v4_pro"


def test_risk_classifier_auth_path():
    routing = ModelRouting(CONFIG)
    assert routing.is_high_risk(paths=["backend/auth/jwt.py"])
    assert routing.is_high_risk(task_description="Add rls policy for tenants")
    assert not routing.is_high_risk(paths=["backend/health.py"], task_description="health check")


def test_minimax_primary_when_key_present(settings_or_only):
    settings_or_only.minimax_api_key = "mm-test"
    router = ModelRouter(settings_or_only, conn=None)
    router.config_dir = CONFIG
    router.registry = ModelRegistry(CONFIG)
    router.routing = ModelRouting(CONFIG)
    router.fallbacks = ProviderFallbacks(CONFIG)

    resolved = router.resolve("backend")
    assert resolved.provider == "minimax_official"
    assert resolved.api_key == "mm-test"


def test_any_provider_key(settings_or_only):
    assert any_provider_key(settings_or_only)
    settings_or_only.openrouter_api_key = ""
    assert not any_provider_key(settings_or_only)
    assert api_key_for(settings_or_only, "openrouter") == ""


def test_log_llm_call_accepts_source():
    import inspect
    from jarvis.db import store

    assert "source" in inspect.signature(store.log_llm_call).parameters
