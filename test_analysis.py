import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analysis import (CONDITIONS, aggregate_trials, exact_mcnemar,
                      executive_markdown, paired_from_all_success_aggregate,
                      paired_from_trials, read_published, rollup, validate_trials,
                      wilson_interval)


def test_published_data_provenance_and_correct_totals():
    d = read_published()
    assert len(d) == 12
    out = rollup(d).set_index("condition")
    for condition, count in zip(CONDITIONS, [64,65,69,90]):
        assert out.loc[condition, "selected"] == count
        assert out.loc[condition, "total"] == 90
    assert d.groupby("model")["total"].sum().to_dict() == {"ChatGPT":120, "Claude":120, "Gemini":120}


def test_model_counts():
    d = read_published().set_index(["model", "condition"])
    assert d.loc[("Gemini", "Control"), "selected"] == 11
    assert d.loc[("Gemini", "Request Language Only"), "selected"] == 12
    assert d.loc[("Claude", "Neutral Copy"), "selected"] == 25
    assert d.loc[("ChatGPT", "Neutral Copy"), "selected"] == 29


def test_mcnemar_exact_when_one_arm_is_all_success():
    d = read_published()
    p = paired_from_all_success_aggregate(d, "Request Language Only", "Product-to-Use Relationship")
    assert p["n"] == 90
    assert (p["improved"], p["worsened"]) == (21,0)
    assert p["p"] == pytest.approx(2 * .5**21)
    assert paired_from_all_success_aggregate(d, "Control", "Neutral Copy") is None


def test_reversed_full_success_pair_comparison():
    p = paired_from_all_success_aggregate(read_published(), "Product-to-Use Relationship", "Control")
    assert (p["improved"],p["worsened"]) == (0,26)
    assert p["p"] == pytest.approx(2 * .5**26)


def test_binomial_intervals_are_bounded():
    lo, hi = wilson_interval(90, 90)
    assert 0.95 < lo < 1
    assert hi == 1.0
    assert exact_mcnemar(0, 0) == 1


def test_upload_canonicalization_and_exact_pairing():
    d = pd.DataFrame([
        ["Gemini", "keyword only", "01", "0", "blinded", "not selected"],
        ["Gemini", "relationship", "01", "yes", "blinded", "target selected"],
        ["Gemini", "keyword only", "02", "1", "blinded", "target selected"],
        ["Gemini", "relationship", "02", "1", "blinded", "target selected"],
        ["Gemini", "keyword only", "03", "1", "blinded", "third trial"],
    ], columns=["model", "condition", "trial_id", "selected", "mode", "raw_response"])
    clean = validate_trials(d)
    p = paired_from_trials(clean, "Request Language Only", "Product-to-Use Relationship")
    assert p["n"] == 2
    assert p["unmatched"] == 1
    assert (p["improved"], p["worsened"]) == (1,0)
    assert p["p"] == 1
    assert aggregate_trials(clean)["total"].sum() == 5


def test_reject_duplicate_pair_key_and_missing_selected():
    d = pd.DataFrame({"model":["Claude","Claude"], "condition":["control","control"],
                      "trial_id":[1,1], "selected":[1,0]})
    with pytest.raises(ValueError, match="repeated"):
        validate_trials(d)
    d = d.iloc[:1].copy()
    d["selected"] = d["selected"].astype(str)
    d.loc[:,"selected"] = "maybe"
    with pytest.raises(ValueError, match="binary"):
        validate_trials(d)


def test_report_describes_limits():
    d = read_published()
    p = paired_from_all_success_aggregate(d, CONDITIONS[2], CONDITIONS[3])
    text = executive_markdown(d, source_label="Public", models=list(["ChatGPT","Claude","Gemini"]),
                              mode="blinded", before=CONDITIONS[2], after=CONDITIONS[3], pairs=p)
    assert "69/90" in text
    assert "90/90" in text
    assert "21" in text
    assert "live" in text
