"""Data integrity and statistics for the Summer in a Bottle explorer.

Published rows are aggregates, not reconstructed raw responses.
Comparisons requiring pairing only use source-backed all-success margins
or an explicitly paired, uploaded trial-level CSV.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
from scipy.stats import binomtest

CONDITIONS = (
    "Control",
    "Neutral Copy",
    "Request Language Only",
    "Product-to-Use Relationship",
)
MODEL_ORDER = ("ChatGPT", "Claude", "Gemini")
SOURCE_URL = (
    "https://www.5wpr.com/new/"
    "how-wineries-can-increase-ai-wine-recommendations-a-controlled-study-of-product-to-use-content/"
)
INTERVENTIONS = {
    "Control": "No added sentence.",
    "Neutral Copy": "[Product] should be served chilled when poured.",
    "Request Language Only": "Summer dinner party traditions vary by region and season.",
    "Product-to-Use Relationship": "[Product] is suitable for a summer dinner party.",
}


def read_published(path: str | Path | None = None) -> pd.DataFrame:
    if path is None:
        path = Path(__file__).parent / "data" / "published_summary.csv"
    data = pd.read_csv(path)
    required = {"model", "condition", "selected", "total"}
    if not required.issubset(data.columns):
        raise ValueError("Published data is missing columns")
    if len(data) != 12 or data["selected"].sum() != 288 or data["total"].sum() != 360:
        raise ValueError("Published aggregates fail expected count checks")
    return data


def normalize_condition(value: object) -> str:
    text = re.sub(r"[^a-z0-9]+", " ", str(value).strip().lower()).strip()
    aliases = {
        "control": CONDITIONS[0], "baseline": CONDITIONS[0],
        "neutral": CONDITIONS[1], "neutral copy": CONDITIONS[1], "placebo": CONDITIONS[1],
        "keyword": CONDITIONS[2], "keyword only": CONDITIONS[2],
        "request language only": CONDITIONS[2], "request only": CONDITIONS[2],
        "relationship": CONDITIONS[3], "explicit": CONDITIONS[3],
        "product to use relationship": CONDITIONS[3], "product use relationship": CONDITIONS[3],
        "explicit relationship": CONDITIONS[3],
    }
    if text not in aliases:
        raise ValueError(f"Unrecognized condition: {value!r}")
    return aliases[text]


def _as_binary(value: object) -> int:
    if pd.isna(value):
        raise ValueError("Missing selected value")
    text = str(value).strip().lower()
    if text in {"1", "1.0", "true", "t", "yes", "y", "selected"}:
        return 1
    if text in {"0", "0.0", "false", "f", "no", "n", "not selected"}:
        return 0
    raise ValueError(f"selected must be binary, got {value!r}")


def validate_trials(raw: pd.DataFrame) -> pd.DataFrame:
    """Validate uploaded genuine trial observations; never fill missing rows."""
    df = raw.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    if "selected" not in df and "target_selected" in df:
        df = df.rename(columns={"target_selected": "selected"})
    required = {"model", "condition", "trial_id", "selected"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError("Missing required column(s): " + ", ".join(missing))
    if len(df) == 0:
        raise ValueError("The CSV has no trial rows; use a completed trial export.")
    for col in ["model", "condition", "trial_id"]:
        if df[col].isna().any() or df[col].astype(str).str.strip().eq("").any():
            raise ValueError(f"{col} cannot contain blank values")
    df["model"] = df["model"].astype(str).str.strip()
    df["trial_id"] = df["trial_id"].astype(str).str.strip()
    df["condition"] = df["condition"].map(normalize_condition)
    df["selected"] = df["selected"].map(_as_binary).astype(int)
    if "mode" in df.columns:
        df["mode"] = df["mode"].fillna("not specified").astype(str).str.strip().str.lower()
    else:
        df["mode"] = "not specified"
    keys = ["mode", "model", "trial_id", "condition"]
    if df.duplicated(keys).any():
        n = int(df.duplicated(keys).sum())
        raise ValueError(f"{n} repeated model/mode/trial_id/condition keys; cannot identify unique observations")
    if "target_rank" in df.columns:
        df["target_rank"] = pd.to_numeric(df["target_rank"], errors="coerce")
        if ((df["selected"] == 1) & df["target_rank"].notna() & (df["target_rank"] < 1)).any():
            raise ValueError("target_rank must be >= 1 for selected products")
    return df


def aggregate_trials(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby(["model", "condition"], as_index=False).agg(
        selected=("selected", "sum"), total=("selected", "count")
    )
    result["source_type"] = "uploaded_trial_rows"
    return result


def rollup(aggregate: pd.DataFrame, models: list[str] | None = None) -> pd.DataFrame:
    if models is not None:
        aggregate = aggregate.loc[aggregate["model"].isin(models)]
    result = (
        aggregate.groupby("condition", as_index=False)[["selected", "total"]]
        .sum().set_index("condition").reindex(CONDITIONS).fillna(0).reset_index()
    )
    result[["selected", "total"]] = result[["selected", "total"]].astype(int)
    result["rate"] = result.apply(
        lambda row: row.selected / row.total if row.total else float("nan"), axis=1
    )
    return result


def wilson_interval(success: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """95% Wilson score interval for a single binomial proportion (descriptive only)."""
    if total <= 0:
        return float("nan"), float("nan")
    p = success / total
    den = 1 + z * z / total
    center = (p + z * z / (2 * total)) / den
    radius = z / den * ((p * (1 - p) / total + z * z / (4 * total * total)) ** 0.5)
    return max(0.0, center - radius), min(1.0, center + radius)


def exact_mcnemar(improved: int, worsened: int) -> float:
    """Two-sided exact McNemar p from discordant pair counts."""
    if improved < 0 or worsened < 0:
        raise ValueError("Discordances cannot be negative")
    n = improved + worsened
    return float(binomtest(min(improved, worsened), n, p=0.5, alternative="two-sided").pvalue) if n else 1.0


def paired_from_trials(
    df: pd.DataFrame, before: str, after: str, models: list[str] | None = None
) -> dict:
    """Only compare matched model + mode + trial_id; no positional guessing."""
    data = df[df["condition"].isin([before, after])]
    if models is not None:
        data = data[data["model"].isin(models)]
    pivot = data.pivot(index=["mode", "model", "trial_id"], columns="condition", values="selected")
    if before not in pivot.columns or after not in pivot.columns:
        return {"n": 0, "unmatched": len(pivot), "improved": 0, "worsened": 0,
                "stayed_selected": 0, "stayed_unselected": 0, "p": None}
    matched = pivot.dropna(subset=[before, after])
    b = matched[before].astype(int)
    a = matched[after].astype(int)
    up = int(((b == 0) & (a == 1)).sum())
    down = int(((b == 1) & (a == 0)).sum())
    return {
        "n": len(matched), "unmatched": len(pivot) - len(matched),
        "improved": up, "worsened": down,
        "stayed_selected": int(((b == 1) & (a == 1)).sum()),
        "stayed_unselected": int(((b == 0) & (a == 0)).sum()),
        "p": exact_mcnemar(up, down),
    }


def paired_from_all_success_aggregate(aggregate: pd.DataFrame, before: str, after: str) -> dict | None:
    """Only infer paired flips if one arm succeeds for all matched trials.

    The published study states these are matched trials; therefore an all-yes
    condition logically rules out any negative flips against that condition.
    No other marginal-only comparison is made.
    """
    r = rollup(aggregate).set_index("condition")
    if before not in r.index or after not in r.index:
        return None
    n0, n1 = int(r.loc[before, "total"]), int(r.loc[after, "total"])
    if n0 <= 0 or n0 != n1:
        return None
    k0, k1 = int(r.loc[before, "selected"]), int(r.loc[after, "selected"])
    if k1 == n1:
        up, down = n0 - k0, 0
    elif k0 == n0:
        up, down = 0, n1 - k1
    else:
        return None
    return {
        "n": n0, "unmatched": 0, "improved": up, "worsened": down,
        "stayed_selected": min(k0, k1), "stayed_unselected": 0,
        "p": exact_mcnemar(up, down), "inferred_from_all_success": True,
    }


def executive_markdown(
    agg: pd.DataFrame, *, source_label: str, models: list[str], mode: str,
    before: str, after: str, pairs: dict | None,
) -> str:
    summary = rollup(agg, models).set_index("condition")
    k0, n0 = int(summary.loc[before, "selected"]), int(summary.loc[before, "total"])
    k1, n1 = int(summary.loc[after, "selected"]), int(summary.loc[after, "total"])
    r0 = k0 / n0 if n0 else 0
    r1 = k1 / n1 if n1 else 0
    delta = (r1 - r0) * 100
    lines = [
        "# AI Recommendation Experiment — Executive Brief",
        "",
        f"**Data:** {source_label} | **Mode:** {mode} | **Models:** {', '.join(models)}",
        "",
        "**Research question:** Does linking Summer in a Bottle to the occasion in a consumer's request change its selection rate?",
        "",
        "## Comparison",
        f"- Before: {before} — {k0}/{n0} ({r0:.1%})",
        f"- After: {after} — {k1}/{n1} ({r1:.1%})",
        f"- Difference: {delta:+.1f} percentage points (observed selected-rate difference)",
        "",
        "## Results by condition",
        "| Condition | Selected | Trials | Rate |",
        "|---|---:|---:|---:|",
    ]
    for _, row in summary.reset_index().iterrows():
        rate = f"{row['selected']/row['total']:.1%}" if row["total"] else "n/a"
        lines.append(f"| {row['condition']} | {int(row['selected'])} | {int(row['total'])} | {rate} |")
    lines += ["", "## Paired evidence"]
    if pairs is not None and pairs.get("p") is not None and pairs.get("n", 0) > 0:
        lines += [
            f"- Matched pairs: {pairs['n']}",
            f"- Moved toward target: {pairs['improved']}",
            f"- Moved away from target: {pairs['worsened']}",
            f"- Exact two-sided McNemar p-value: {pairs['p']:.6g}",
        ]
        if pairs.get("inferred_from_all_success"):
            lines.append("- Pair directions derived from the published all-success condition and stated paired design; individual rows are not reconstructed.")
        elif pairs.get("unmatched", 0):
            lines.append(f"- Unmatched uploaded trial keys excluded: {pairs['unmatched']}")
    else:
        lines.append("- Paired significance cannot be derived from marginal counts for this comparison. Upload genuine paired trials.")
    lines += [
        "", "## Interpretation", "",
        "In this controlled, eight-wine, top-three selection task, supplying explicit product-to-occasion evidence increased the target's selection rate. The results do not measure live search discovery, retrieval, crawling, or recommendation probability for real consumers.",
        "", "## Source and limitations", "",
        f"Study: {SOURCE_URL}",
        "Published aggregate data contain no original per-trial responses, ranks, seeds, or candidate positions.",
        "When using uploaded rows, the report summarizes the user's input; independently verify provenance and experimental design.",
    ]
    return "\n".join(lines) + "\n"
