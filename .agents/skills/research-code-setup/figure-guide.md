# Figure Guide

How to choose and design charts of research results. Plotting code lives in `code/src` and runs through `python scripts/research.py run`, so every figure has a recorded run. The researcher's confirmed rules and the venue's figure requirements take precedence over this guide.

## Recommend a form

When the researcher asks which chart suits a result, answer in three parts:

1. **Recommended form.** One form, and at most one alternative.
2. **Reason.** The one statement the figure must support, and why this form shows that statement for this data.
3. **Design.** The axes (meaning and units), the scale, how uncertainty is shown, the marks and colors of each series, and the file format.

Decide the statement first, then choose the form.

## Choose by the statement

| The figure must show | Usual form | Notes |
| --- | --- | --- |
| A few methods compared on one measure | Dot plot or vertical bars | Bars start at zero; a dot plot allows a narrower axis. |
| Many methods, tasks, or settings at once | A table, a heatmap with printed values, or small multiples | A table is better when readers need exact values. |
| A trend over training steps or a parameter | Line chart | Shade the spread across runs. |
| Converging curves whose final gap matters | Line chart with a zoomed inset or a second panel | Say in the caption what the inset enlarges. |
| A trade-off between two measures (accuracy and cost) | Scatter plot that marks the Pareto front, the points that no other point beats on both measures | Label the points with method names. |
| Three measures at once (for example accuracy, cost, and model size) | Bubble chart, where bubble size shows the third measure | Keep the size scale fixed across panels, and label the bubbles. |
| Two measures with different units across the same categories | Two aligned panels | A combined bar-and-line chart with two axes is hard to read. Use it only when the two series must be read against each other. |
| A distribution across runs or samples | Box plot or violin plot | Show the individual points when there are few. |
| The relation between two continuous variables | Scatter plot | Add a fitted curve only when its model is stated. |
| Agreement between predicted and observed values | Scatter plot with the identity line | |
| Parts of a whole | Stacked bars; a donut chart for two or three parts | Avoid a pie chart with many slices. |
| Performance across classification thresholds | ROC curve for balanced classes; precision-recall curve when positives are rare | |
| A profile of several criteria for one or two methods | Radar chart only for three to five criteria on normalized scales; otherwise a dot plot | The area of a radar chart depends on the order of its axes, so readers compare shapes poorly. |

## Fit the data

- Long labels or many categories: horizontal bars, so that labels stay readable.
- Too many series for one panel: small multiples with shared axes.
- Different units: aligned panels with a shared x-axis. Use two y-axes only when the series must be read against each other at the same x value, and label both axes.
- Values across orders of magnitude, or multiplicative change: a logarithmic axis, labeled as such.
- Change relative to a baseline: plot the relative change against a stated baseline, and write the formula in the caption.
- Groups at very different levels: separate panels, or the relative change. Use a broken axis rarely, and mark the break.

## Show uncertainty honestly

- For repeated runs, seeds, or samples, show the spread. Say in the caption which measure it is (standard deviation, standard error, or a confidence interval) and how many runs it covers.
- For a single run, draw no error bars, and say that it is a single run.
- Mark a statistical difference only for a test that the result record reports.
- Plot what the result record holds. Never leave out runs to make a difference look larger.

## Style

- Use a palette that readers with color-vision deficiency can distinguish. Separate the series by marker or line style as well, so that the figure survives grayscale printing.
- Keep each method's color and marker the same in every figure of the paper.
- Make the text readable at the printed size, close to the caption size, and give the axis labels with their units.
- Save plots in a vector format (PDF or SVG). Save raster images at the resolution that the venue requires.
- Leave out 3D effects, shadows, and decorative backgrounds. Use light gridlines at most.
- Give each figure one message. Move secondary detail to supplementary material.
- Check the figure in grayscale and at print size before it enters the manuscript.

## Tables

- Put the direction of each metric in its column header, for example "higher is better" or an arrow, so that readers can compare the columns without reading the text.
- Align the numbers on the decimal point, and use the same number of decimals within a column.
- Mark the best value of a column only when the venue permits it, and say in the caption what the mark means.
- Keep the table light: few rules, no shading. The output profile sets the final table style.

## Hand-off

Place the figure that the manuscript uses in `manuscript/assets/`, or in the candidate's `assets/` when `manuscript-revision` supplied that target; a staged figure must not replace an active manuscript asset before application. Write its caption under the [editing guide](../manuscript-writing/editing-guide.md#captions-and-table-titles) and the workspace conventions.
