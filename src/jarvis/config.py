from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openrouter_api_key: str = ""
    supabase_url: str = "https://bbckbcusqbdgcxnnimus.supabase.co"
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    supabase_secret_key: str = ""
    database_url: str = ""
    jarvis_projects_root: str = "projects"
    worker: str = "fallback"
    task_timeout_sec: int = 1800
    daily_spend_cap_usd: float = 20.0
    tier0_model: str = "openai/gpt-4o-mini"
    tier1_model: str = "openai/gpt-4o-mini"
    tier2_model: str = "anthropic/claude-sonnet-4"
    tier3_model: str = "anthropic/claude-opus-4"


def get_settings() -> Settings:
    return Settings()
