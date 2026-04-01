# Gender and Parental Education Effects on Student Test Performance

Application report for the **M.Sc. Data Science** programme at TU Dortmund University (Winter Semester 2026/2027).

## Overview

This report analyses the performance of 486 students in Mathematics and Language, investigating two research questions:

1. **Gender differences** — Is there a statistically significant difference between male and female students in their Mathematics and Language scores?
2. **Parental education differences** — Do test scores differ across parental education levels? If so, which groups differ from each other?

## Key Findings

- Males score significantly higher in Mathematics (*t*(484) = −3.78, *p* < 0.001, *d* = −0.34)
- Females score significantly higher in Language (*t*(484) = 6.41, *p* < 0.001, *d* = 0.58)
- Students whose parents have only a high school education score significantly lower in both subjects than all other groups
- The critical threshold lies between no post-secondary education and any tertiary qualification

## Repository Contents

| File | Description |
|------|-------------|
| `report.pdf` | Final application report (PDF) |
| `analysis.ipynb` | Jupyter notebook with the complete analysis code |
| `Scores.csv` | Dataset provided by TU Dortmund |
| `figure1_gender_boxplot.png` | Boxplot of scores by gender |
| `figure2_education_boxplot.png` | Boxplot of scores by parental education |

## Methods

- **Descriptive statistics**: mean, median, SD, IQR, boxplots
- **Assumption checks**: Shapiro-Wilk (normality), Levene's test (homogeneity of variance)
- **RQ1**: Two-sample Student's *t*-test with Cohen's *d*
- **RQ2 Mathematics**: Kruskal-Wallis test + Dunn's post-hoc (Bonferroni correction)
- **RQ2 Language**: One-way ANOVA + Tukey's HSD

## Requirements

```
pip install pandas numpy scipy matplotlib seaborn scikit-posthocs statsmodels
```

## Author

Hira Rehman 
