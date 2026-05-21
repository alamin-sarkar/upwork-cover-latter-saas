from __future__ import annotations

import sys
from pathlib import Path


def ensure_ai_workflows_importable() -> None:
    """Allow local monorepo runs to import ai_workflows without reinstalling."""
    try:
        __import__("ai_workflows")
        return
    except ModuleNotFoundError as exc:
        if exc.name != "ai_workflows":
            raise

    package_src = (
        Path(__file__).resolve().parents[4] / "packages" / "ai-workflows" / "src"
    )
    src_path = str(package_src)
    if package_src.is_dir() and src_path not in sys.path:
        sys.path.insert(0, src_path)


ensure_ai_workflows_importable()
