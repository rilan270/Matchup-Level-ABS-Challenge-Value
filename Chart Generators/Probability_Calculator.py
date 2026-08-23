import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os

#Load the 432-situation higher-RE probability table

matplotlib.rcParams['savefig.dpi'] = 600
script_dir = os.path.dirname(os.path.abspath(__file__))

situations_path = os.path.join(
    script_dir,
    "..",
    "Probability with RE24",
    "situationHigherREProbability_AllGames_432.csv"
)

situations_df = pd.read_csv(situations_path)

#Ask which half-inning to chart

print("\nType in inning number (1-9)")
inning_input = int(input())

print("\nType in Top or Bot")
half_input = input().strip().lower()

if half_input in ("top", "t"):
    half_label = "Top"
elif half_input in ("bot", "bottom", "b"):
    half_label = "Bot"
else:
    raise ValueError(
        f"Unrecognized half-inning input: '{half_input}'. "
        f"Use Top or Bot."
    )

if inning_input not in range(1, 10):
    raise ValueError(
        f"Inning must be 1-9, got {inning_input}."
    )

half_inning_df = situations_df[
    (situations_df["inning"] == inning_input)
    & (situations_df["inning_topbot"].astype(str) == half_label)
].copy()

if len(half_inning_df) != 24:
    raise ValueError(
        f"Expected 24 rows for inning {inning_input} {half_label}, "
        f"found {len(half_inning_df)}."
    )

base_order = [
    "000",  # empty
    "100",  # runner on 1st
    "010",  # runner on 2nd
    "001",  # runner on 3rd
    "110",  # 1st & 2nd
    "101",  # 1st & 3rd
    "011",  # 2nd & 3rd
    "111",  # bases loaded
]

half_inning_df["base_state"] = (
    half_inning_df["1b"].astype(int).astype(str)
    + half_inning_df["2b"].astype(int).astype(str)
    + half_inning_df["3b"].astype(int).astype(str)
)

half_inning_df["base_state"] = pd.Categorical(
    half_inning_df["base_state"],
    categories=base_order,
    ordered=True
)

pct_table = half_inning_df.pivot_table(
    values="higher_re_occurs_pct",
    index="base_state",
    columns="outs_when_up",
    aggfunc="mean",
    observed=False
)

# Explicit ordering
pct_table = pct_table.reindex(
    index=base_order,
    columns=[0, 1, 2]
)

pct_table.columns = [
    "0 outs",
    "1 out",
    "2 outs"
]

# Plotting

colors = plt.cm.bwr(np.linspace(0, 1, 256))
colors[:, :3] = colors[:, :3] * 0.6 + 0.4

pastel_cmap = LinearSegmentedColormap.from_list("pastel_bwr", colors).reversed()


def format_bases_from_state(state):
    return (
        f"{'1B' if state[0] == '1' else '—'} "
        f"{'2B' if state[1] == '1' else '—'} "
        f"{'3B' if state[2] == '1' else '—'}"
    )


def plot_re_table(
    table,
    fig_title,
    subtitle=None,
    pct_format=False
):
    row_labels = [
        format_bases_from_state(str(state))
        for state in table.index
    ]

    fig, ax = plt.subplots(figsize=(3.2, 5))
    ax.axis("off")

    if pct_format:
        fmt = lambda x: (
            f"{x:.1%}"
            if not np.isnan(x)
            else ""
        )
    else:
        fmt = lambda x: (
            f"{x:.3f}"
            if not np.isnan(x)
            else ""
        )

    t = ax.table(
        cellText=[
            [fmt(x) for x in row]
            for row in table.values
        ],
        rowLabels=row_labels,
        colLabels=table.columns,
        cellLoc="center",
        loc="center",
        bbox=[0.25, 0, 0.75, 0.8]
    )

    valid_values = table.values[
        ~np.isnan(table.values)
    ]

    if len(valid_values) > 0:

        vmin = np.percentile(valid_values, 1)
        vcenter = np.percentile(valid_values, 50)
        vmax = np.percentile(valid_values, 99)

        if vmin == vcenter:
            vmin = vcenter - 0.000001

        if vmax == vcenter:
            vmax = vcenter + 0.000001

        norm = matplotlib.colors.TwoSlopeNorm(
            vmin=vmin,
            vcenter=vcenter,
            vmax=vmax
        )

    cells = t.get_celld()

    #cell widths

    for (row, col), cell in cells.items():

        if col == -1:
            cell.set_width(0.2)
        else:
            cell.set_width(0.05)

    for (row, col), cell in cells.items():

        # Column headers
        if row == 0:
            cell.set_facecolor("black")
            cell.set_text_props(
                color="white",
                weight="bold"
            )

        # Row labels
        elif col == -1:
            cell.set_facecolor("black")
            cell.set_text_props(
                color="white",
                weight="bold"
            )

        else:
            actual_row = row - 1
            value = table.iloc[actual_row, col]

            if not np.isnan(value):
                color = pastel_cmap(norm(value))
                cell.set_facecolor(color)

    t.auto_set_font_size(False)
    t.set_fontsize(9)
    t.scale(1, 1.2)

    plt.suptitle(
        fig_title,
        fontsize=14,
        fontweight="bold",
        y=0.98
    )

    if subtitle:
        plt.figtext(
            0.5,
            0.90,
            subtitle,
            fontsize=10,
            ha="center",
            va="top"
        )

    plt.subplots_adjust(top=0.86)


# Probability for this half-inning

total_occurrences = (
    half_inning_df["eligible_games"].sum()
)

total_higher_re = (
    half_inning_df["higher_re_occurs_count"].sum()
)

avg_pct = (
    total_higher_re / total_occurrences
    if total_occurrences > 0
    else np.nan
)

if inning_input == 1:
    suffix = "st"
elif inning_input == 2:
    suffix = "nd"
elif inning_input == 3:
    suffix = "rd"
else:
    suffix = "th"

# Plot
        
plot_re_table(
    pct_table,
    fig_title=(
        f"{half_label} {inning_input}{suffix}"
    ),
    subtitle=(
        f"Probability at least one greater RE24 \n"
        f"situation occurs after the current PA\n"
        f"Average for Inning: {avg_pct:.1%}"
    ),
    pct_format=True
)

plt.show()