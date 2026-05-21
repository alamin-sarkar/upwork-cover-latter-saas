import sys
from pathlib import Path

from app.core.workspace_imports import ensure_ai_workflows_importable


def test_ensure_ai_workflows_importable_adds_monorepo_src_when_missing(monkeypatch):
    root = Path(__file__).resolve().parents[3]
    expected_src = root / "packages" / "ai-workflows" / "src"
    src_text = str(expected_src)

    monkeypatch.setattr(sys, "path", [entry for entry in sys.path if entry != src_text])
    monkeypatch.delitem(sys.modules, "ai_workflows", raising=False)

    ensure_ai_workflows_importable()

    assert sys.path[0] == src_text


def test_ensure_ai_workflows_importable_no_duplicate_path(monkeypatch):
    root = Path(__file__).resolve().parents[3]
    expected_src = str(root / "packages" / "ai-workflows" / "src")

    monkeypatch.setattr(sys, "path", [expected_src, *[entry for entry in sys.path if entry != expected_src]])
    monkeypatch.delitem(sys.modules, "ai_workflows", raising=False)

    ensure_ai_workflows_importable()

    assert sys.path.count(expected_src) == 1
