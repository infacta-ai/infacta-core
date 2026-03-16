from core.core_engine import run_core


def analyze(text: str, mode: str = "document") -> dict:
    return run_core(text, mode=mode)
