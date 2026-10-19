from pathlib import Path
from lip_data import TARGET_A, MODEL_COUNTS, COMPETITION, validate_published_lip_counts
from visibility_data import ratios


def test_published_lip_data():
    assert validate_published_lip_counts() is True
    assert int(TARGET_A.loc[TARGET_A.condition=="Explicit suitability", "selected"].iloc[0]) == 87
    assert int(MODEL_COUNTS.keyword_selected.sum()) == 47
    assert int(COMPETITION.selected.sum()) == 90


def test_visibility_arithmetic():
    rates = ratios(69,25,71)
    assert round(100*rates["appearance_rate"],2) == 97.18
    assert round(100*rates["first_position_rate"],2) == 35.21
    assert round(rates["difference_pp"],2) == 61.97


def test_invalid_visibility_counts():
    try:
        ratios(5,7,10)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid numerator relationship was accepted")


def test_public_page_read_only():
    public_view = Path(__file__).parent / "wine_explorer.py"
    content = public_view.read_text()
    assert "st.file_uploader(" not in content
    assert "using_published = True" in content
