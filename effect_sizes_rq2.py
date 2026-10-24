"""Effect sizes for RQ2 (parental education).

The report establishes that scores differ across parental education levels. A p-value says the
difference is unlikely to be chance; it does not say how large the difference is. This script adds
that missing piece:

  Mathematics (Kruskal-Wallis)  -> epsilon-squared
  Language    (one-way ANOVA)   -> eta-squared and omega-squared

RQ1 is recomputed at the end as a check that this script reproduces the figures already in the
report, so the new numbers can be trusted to come from the same pipeline.

Run from the repository root:
    python effect_sizes_rq2.py
"""

import numpy as np
import pandas as pd
from scipy import stats

CSV = "Scores.csv"
EDU_ORDER = [
    "high school",
    "associate's degree",
    "bachelor's degree",
    "master's degree",
]


def load() -> pd.DataFrame:
    """Load the long-format file and return one row per student.

    The file is semicolon-separated and uses a comma as the decimal mark (for example 80,5),
    so both have to be declared or the language scores silently come back as strings.
    """
    raw = pd.read_csv(CSV, sep=";", quotechar='"', index_col=0, decimal=",")
    raw.columns = [c.strip() for c in raw.columns]

    wide = raw.pivot_table(
        index=["student_id", "gender", "parental.level.of.education"],
        columns="subject",
        values="score",
        aggfunc="first",
    ).reset_index()
    wide.columns.name = None
    wide = wide.rename(columns={"math": "math_score", "language": "language_score"})
    for col in ("math_score", "language_score"):
        wide[col] = wide[col].astype(float)
    return wide


def epsilon_squared(h: float, n: int, k: int) -> float:
    """Epsilon-squared for Kruskal-Wallis: (H - k + 1) / (n - k).

    Interpreted as the proportion of variability in the ranks explained by the grouping.
    """
    return (h - k + 1) / (n - k)


def anova_effect_sizes(groups, values):
    """Return (eta-squared, omega-squared, MS_within) for a one-way ANOVA."""
    n, k = len(values), len(groups)
    grand = values.mean()
    ss_between = sum(len(g) * (g.mean() - grand) ** 2 for g in groups)
    ss_total = ((values - grand) ** 2).sum()
    ss_within = ss_total - ss_between
    ms_within = ss_within / (n - k)
    eta2 = ss_between / ss_total
    omega2 = (ss_between - (k - 1) * ms_within) / (ss_total + ms_within)
    return eta2, omega2, ms_within


def main() -> None:
    df = load()
    n, k = len(df), len(EDU_ORDER)
    print(f"{n} students, {k} parental education groups\n")

    # ---- RQ2 Mathematics: Kruskal-Wallis, assumptions for ANOVA were not met
    math_groups = [
        df.loc[df["parental.level.of.education"] == e, "math_score"].to_numpy(dtype=float)
        for e in EDU_ORDER
    ]
    h, p = stats.kruskal(*math_groups)
    eps2 = epsilon_squared(h, n, k)
    print("RQ2 Mathematics, Kruskal-Wallis")
    print(f"  H({k - 1}) = {h:.2f}, p = {p:.2e}")
    print(f"  epsilon-squared = {eps2:.3f}  ({eps2 * 100:.1f}% of rank variance)")
    for e, g in zip(EDU_ORDER, math_groups):
        print(f"    {e:<22} n={len(g):>3}  median={np.median(g):>5.1f}  mean={g.mean():>6.2f}")
    print()

    # ---- RQ2 Language: one-way ANOVA, assumptions held
    lang_groups = [
        df.loc[df["parental.level.of.education"] == e, "language_score"].to_numpy(dtype=float)
        for e in EDU_ORDER
    ]
    f_stat, p = stats.f_oneway(*lang_groups)
    values = df["language_score"].to_numpy(dtype=float)
    eta2, omega2, ms_within = anova_effect_sizes(lang_groups, values)
    print("RQ2 Language, one-way ANOVA")
    print(f"  F({k - 1}, {n - k}) = {f_stat:.2f}, p = {p:.2e}")
    print(f"  eta-squared   = {eta2:.3f}  ({eta2 * 100:.1f}% of total variance)")
    print(f"  omega-squared = {omega2:.3f}  (less upward bias than eta-squared)")
    print(f"  MS_within = {ms_within:.2f}")
    for e, g in zip(EDU_ORDER, lang_groups):
        print(f"    {e:<22} n={len(g):>3}  mean={g.mean():>6.2f}  sd={g.std(ddof=1):>5.2f}")
    print()

    # ---- RQ1, recomputed purely as a check against the published report
    print("RQ1 check, should match the report")
    for col, label in (("math_score", "Mathematics"), ("language_score", "Language")):
        male = df.loc[df["gender"] == "male", col].to_numpy(dtype=float)
        female = df.loc[df["gender"] == "female", col].to_numpy(dtype=float)
        t, p = stats.ttest_ind(female, male, equal_var=True)
        n_f, n_m = len(female), len(male)
        pooled_sd = np.sqrt(
            ((n_f - 1) * female.var(ddof=1) + (n_m - 1) * male.var(ddof=1)) / (n_f + n_m - 2)
        )
        d = (female.mean() - male.mean()) / pooled_sd
        print(f"  {label:<12} t({n_f + n_m - 2}) = {t:+.2f}, p = {p:.2e}, Cohen's d = {d:+.2f}")


if __name__ == "__main__":
    main()
