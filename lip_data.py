"""Aggregated published 5WPR lip-treatment data; no reconstructed trial rows."""
import pandas as pd

TARGET_A = pd.DataFrame([
    {"condition": "Control", "selected": 0, "total": 90},
    {"condition": "Neutral copy", "selected": 0, "total": 90},
    {"condition": "Keyword only", "selected": 47, "total": 90},
    {"condition": "Explicit suitability", "selected": 87, "total": 90},
])

MODEL_COUNTS = pd.DataFrame([
    {"model": "ChatGPT", "keyword_selected": 15, "explicit_selected": 27, "trials": 30},
    {"model": "Claude", "keyword_selected": 6, "explicit_selected": 30, "trials": 30},
    {"model": "Gemini", "keyword_selected": 26, "explicit_selected": 30, "trials": 30},
])

COMPETITION = pd.DataFrame([
    {"product": "Target A", "selected": 49, "total": 90},
    {"product": "Target B", "selected": 39, "total": 90},
    {"product": "Peptide comparator", "selected": 2, "total": 90},
])


def validate_published_lip_counts() -> bool:
    assert len(TARGET_A) == 4 and set(TARGET_A.selected.tolist()) == {0,47,87}
    assert int(MODEL_COUNTS.keyword_selected.sum()) == 47
    assert int(MODEL_COUNTS.explicit_selected.sum()) == 87
    assert int(COMPETITION.selected.sum()) == 90
    return True
