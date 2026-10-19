"""Small self-contained arithmetic QA examples from a public GEO measurement article."""

def ratios(appearances: int, first: int, answers: int) -> dict:
    if answers <= 0 or not (0 <= first <= appearances <= answers):
        raise ValueError("Require 0 <= first positions <= appearances <= total answers")
    return {"appearance_rate": appearances / answers,
            "first_position_rate": first / answers,
            "first_given_appearance": first / appearances if appearances else 0,
            "difference_pp": 100 * (appearances-first) / answers}
