# Gender and Parental Education Effects on Student Test Performance

Application report for the **M.Sc. Data Science** programme at TU Dortmund University (Winter Semester 2026/2027).

## Overview

This report analyses the performance of 486 students in Mathematics and Language, investigating two research questions:

1. **Gender differences** — Is there a statistically significant difference between male and female students in their Mathematics and Language scores?
2. **Parental education differences** — Do test scores differ across parental education levels? If so, which groups differ from each other?

The test for each question was chosen by the assumption checks rather than decided in advance, and every result is reported with an effect size alongside the p-value.

## Key findings

- Males score significantly higher in Mathematics, *t*(484) = −3.78, *p* < 0.001, *d* = −0.34
- Females score significantly higher in Language, *t*(484) = 6.41, *p* < 0.001, *d* = 0.58
- Scores rise with parental education in both subjects, and students whose parents have only a high school education score lowest in both
- The parental education effect is **small in Mathematics** (ε² = 0.026) and **moderate in Language** (η² = 0.081). Both are statistically significant, but neither explains much of the variation between individual students
- The critical threshold lies between no post-secondary education and any tertiary qualification

## Results

### RQ1 — Gender

| Subject | Test | Statistic | p | Effect size |
|---|---|---|---|---|
| Mathematics | Student's *t* | *t*(484) = −3.78 | 0.00018 | *d* = −0.34 (small) |
| Language | Student's *t* | *t*(484) = 6.41 | 3.5 × 10⁻¹⁰ | *d* = 0.58 (medium) |

Negative *d* favours males, positive favours females.

### RQ2 — Parental education

| Subject | Test | Statistic | p | Effect size |
|---|---|---|---|---|
| Mathematics | Kruskal-Wallis | *H*(3) = 15.68 | 0.0013 | ε² = 0.026 (2.6% of rank variance) |
| Language | One-way ANOVA | *F*(3, 482) = 14.24 | 6.6 × 10⁻⁹ | η² = 0.081, ω² = 0.076 |

Group means, in ascending order of parental education:

| Parental education | n | Mathematics mean | Language mean |
|---|---|---|---|
| High school | 156 | 62.24 | 63.53 |
| Associate's degree | 177 | 67.81 | 70.02 |
| Bachelor's degree | 94 | 68.44 | 72.06 |
| Master's degree | 59 | 69.75 | 75.53 |

Worth stating plainly: the Language result is highly significant yet explains about 8% of the total variance, and the Mathematics result explains under 3% of the rank variance. Parental education shifts the group averages, but it is a weak predictor of any individual student's score. A p-value alone would have obscured that.

## Repository contents

| File | Description |
|------|-------------|
| `report.pdf` | Final application report |
| `analysis.ipynb` | Jupyter notebook with the complete analysis |
| `effect_sizes_rq2.py` | Standalone script for the RQ2 effect sizes, with RQ1 recomputed as a check |
| `Scores.csv` | Dataset provided by TU Dortmund |
| `requirements.txt` | Dependencies |
| `figure1_gender_boxplot.png` | Boxplot of scores by gender |
| `figure2_education_boxplot.png` | Boxplot of scores by parental education |

## Methods

- **Descriptive statistics**: mean, median, SD, IQR, boxplots
- **Assumption checks**: Shapiro-Wilk for normality, Levene's test for homogeneity of variance, run before choosing a test
- **RQ1**: two-sample Student's *t*-test with Cohen's *d*
- **RQ2 Mathematics**: Kruskal-Wallis with Dunn's post-hoc and Bonferroni correction, because the normality assumption failed. Effect size reported as epsilon-squared
- **RQ2 Language**: one-way ANOVA with Tukey's HSD, because the assumptions held. Effect size reported as eta-squared and omega-squared

## Running it

```bash
pip install -r requirements.txt
python effect_sizes_rq2.py      # RQ2 effect sizes, plus an RQ1 check against the report
jupyter notebook analysis.ipynb # the full analysis
```

One detail that matters when reading the data: `Scores.csv` is semicolon-separated and uses a comma as the decimal mark, for example `80,5`. Both have to be declared or the Language scores load as strings and fail silently in any numeric step.

## Limitations

- **Cross-sectional and observational.** Nothing here supports a causal reading. Parental education travels with income, school quality and a good deal else that is not in this dataset, so the effects reported are associations.
- **Unequal and small upper groups.** The master's degree group has 59 students against 177 with an associate's degree. The post-hoc comparisons involving the smallest groups have correspondingly less power, so a non-significant pair is not evidence of no difference.
- **Effect sizes are small.** Both RQ2 results are statistically significant and practically modest. With 486 students the study can detect differences that matter little for an individual.
- **Two subjects from one cohort.** The scores come from a single dataset with no information on school, region, cohort year or test conditions, so the findings should not be generalised beyond it.
- **Parental education is treated as four unordered categories.** It is really ordinal, and treating it as nominal discards the ordering. The group means do rise monotonically in both subjects, which a trend test such as Jonckheere-Terpstra could test directly.
- **No correction across research questions.** Bonferroni is applied within the Mathematics post-hoc comparisons and Tukey within Language, but no correction is applied across the four tests as a family.

## Author

Hira Rehman
