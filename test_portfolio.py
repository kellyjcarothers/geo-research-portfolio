from pathlib import Path
from lip_data import TARGET_A, MODEL_COUNTS, COMPETITION, validate_published_lip_counts
import format_data as fd


def test_published_lip_data():
    assert validate_published_lip_counts() is True
    assert int(TARGET_A.loc[TARGET_A.condition=="Explicit suitability", "selected"].iloc[0]) == 87
    assert int(MODEL_COUNTS.keyword_selected.sum()) == 47
    assert int(COMPETITION.selected.sum()) == 90


def _rate(pair):
    n, k = pair
    return round(100 * k / n, 1)


def test_format_design_totals():
    assert fd.DESIGN["cells"] == 2400
    assert sum(n for n, _ in fd.CITATION_COUNTS.values()) == 2400
    assert sum(n for n, _, _ in fd.SONAR_SLOT.values()) == 800
    assert sum(fd.DESIGN["categories"].values()) == fd.DESIGN["facts"] == 40


def test_format_published_figures_reproduce():
    # Figures printed in the August 12, 2026 article.
    assert _rate(fd.CITATION_COUNTS["Perplexity|table"]) == 66.0
    assert _rate(fd.CITATION_COUNTS["Perplexity|diffuse_prose"]) == 55.0
    assert _rate(fd.SONAR_SLOT[1][:2]) == 71.9
    assert _rate(fd.SONAR_SLOT[3][:2]) == 39.4
    published = sorted(_rate(v) for v in fd.CORRECT_VALUE_PUBLISHED.values())
    assert (published[0], published[-1]) == (93.5, 94.6)


def test_format_corrected_scores_only_raise_rates():
    for f, (n, k) in fd.CORRECT_VALUE_CORRECTED.items():
        n0, k0 = fd.CORRECT_VALUE_PUBLISHED[f]
        assert n == n0 and k >= k0


def test_format_paired_counts_consistent():
    for r in fd.SONAR_PAIRED_NAMED:
        a = fd.CITATION_COUNTS[f"Perplexity|{r['a']}"][1]
        b = fd.CITATION_COUNTS[f"Perplexity|{r['b']}"][1]
        assert r["a_only"] - r["b_only"] == a - b
        assert 0 <= r["p"] <= 1


def test_format_data_has_no_response_text():
    names = {k for k in vars(fd) if k.isupper()}
    assert names == {"DESIGN", "CITATION_COUNTS", "CORRECT_VALUE_PUBLISHED", "CORRECT_VALUE_CORRECTED", "SONAR_SLOT",
                     "SONAR_PAIRED_NAMED", "SONAR_NAMED_OR_BRACKET_BY_FORMAT", "HARDER_COUNTS", "CONTRADICTION",
                     "EXAMPLE_PASSAGES"}
    assert "response_text" not in Path(fd.__file__).read_text()


def test_public_page_read_only():
    public_view = Path(__file__).parent / "wine_explorer.py"
    content = public_view.read_text()
    assert "st.file_uploader(" not in content
    assert "using_published = True" in content
