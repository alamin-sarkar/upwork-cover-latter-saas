import app.main as main_module


def test_run_startup_tasks_applies_migrations_when_enabled(monkeypatch):
    called = {"count": 0}

    def fake_apply_migrations() -> None:
        called["count"] += 1

    monkeypatch.setattr(main_module, "apply_migrations", fake_apply_migrations)
    monkeypatch.setattr(main_module.settings, "run_migrations_on_startup", True)

    main_module.run_startup_tasks()

    assert called["count"] == 1


def test_run_startup_tasks_skips_migrations_when_disabled(monkeypatch):
    called = {"count": 0}

    def fake_apply_migrations() -> None:
        called["count"] += 1

    monkeypatch.setattr(main_module, "apply_migrations", fake_apply_migrations)
    monkeypatch.setattr(main_module.settings, "run_migrations_on_startup", False)

    main_module.run_startup_tasks()

    assert called["count"] == 0