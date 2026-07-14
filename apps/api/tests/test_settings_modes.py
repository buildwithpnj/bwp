from app.config import Settings

def test_settings_default_mode():
    s = Settings(mode="development")
    assert s.is_development is True
    assert s.is_production is False

def test_settings_production_mode():
    s = Settings(mode="production")
    assert s.is_development is False
    assert s.is_production is True
