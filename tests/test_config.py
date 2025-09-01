def test_settings_validate_dry_run(tmp_path, monkeypatch):
    monkeypatch.setenv("DRY_RUN", "1")
    monkeypatch.setenv("POST_INTERVAL_MIN_HOURS", "1")
    monkeypatch.setenv("POST_INTERVAL_MAX_HOURS", "2")
    from src.config import Settings

    settings = Settings()
    settings.validate()
    assert settings.dry_run is True


def test_interval_validation(monkeypatch):
    monkeypatch.setenv("DRY_RUN", "1")
    monkeypatch.setenv("POST_INTERVAL_MIN_HOURS", "5")
    monkeypatch.setenv("POST_INTERVAL_MAX_HOURS", "4")
    from src.config import Settings

    s = Settings()
    try:
        s.validate()
        raised = False
    except ValueError:
        raised = True
    assert raised, "should raise on invalid interval"
