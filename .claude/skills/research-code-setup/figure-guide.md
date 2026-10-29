# Figure Guide

How to choose and design charts of research results. Plotting code lives in `code/src` and runs through `python scripts/research.py run`, so that every figure has a recorded run. The researcher's confirmed rules and the venue's figure requirements in the output profile take precedence over this guide.

## Start from the message

Decide the one statement the figure must support, then choose its form.

| The figure must show | Usual form | Notes |
| --- | --- | --- |
| A few methods compared on one measure | Dot chart or vertical bars | Bars start at zero; dots allow a narrower axis. |
| Many methods, tasks, or settings at once | Table, heatmap with printed values, or small multiples | A table is better when readers need exact values. |
| A trend over time, training steps, or a parameter | Line chart | Shade the spread across runs. |
| Two converging curves whose final gap matters | Line chart with an inset or a zoomed second panel | Say in the caption what the inset enlarges. |
| A trade-off between two measures (accuracy and cost, speed and quality) | Scatter plot with the best points connected or marked | Label the points with method names. |
| A distribution | Histogram, box plot, or violin plot | Show the individual points when there are few. |
| The relation between two continuous variables | Scatter plot | Add a fitted curve only when its model is stated. |
| Agreement between predicted and observed values | Scatter plot with the identity line | |
| Parts of a whole | Stacked bars | A pie chart only for two or three parts. |
| A classifier's performance across thresholds | ROC curve for balanced classes, precision-recall curve when positives are rare | |
| Scores on several criteria | Dot plot or heatmap | Radar charts distort areas and are hard to compare. |

## Fit the data

- Long labels or many categories: horizontal bars, so that labels stay level and readable.
- Too many series for one panel: small multiples with shared axes.
- Different units: two aligned panels with a shared x-axis. Use two y-axes only when the series must be read against each other at the same x value, and label both axes.
- Values across orders of magnitude, or multiplicative change: a logarithmic axis, labeled as such.
- Groups at very different levels: show the change relative to a stated baseline, or separate panels. Use a broken axis rarely, and only with a visible break.

## Show uncertainty honestly

- For repeated runs, seeds, or samples, show the spread and say in the caption which measure it is (standard deviation, standard error, or a confidence interval) and how many runs it covers.
- For a single run, draw no error bars, and say that it is a single run.
- Mark a statistical difference only for a test that the result record reports.
- Plot what the result record holds; never leave out runs to make a difference look larger.

## Style

- Use a palette that readers with color-vision deficiency can distinguish, and separate series by marker or line style as well, so that the figure survives grayscale printing.
- Keep each method's color and marker the same in every figure of the paper.
- Make the text readable at the printed size, close to the caption size, and give axis labels with units.
- Save plots in a vector format (PDF or SVG); save raster images at the resolution that the venue requires.
- Leave out 3D effects, shadows, and decorative backgrounds; use light gridlines at most.
- Give each figure one message; move secondary detail to supplementary material.

## Hand-off

Place the figure that the manuscript uses in `manuscript/assets/` and write its caption with the [editing guide](../manuscript-writing/editing-guide.md#captions), under the workspace conventions.
