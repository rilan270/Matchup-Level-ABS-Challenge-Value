import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
situations_path = os.path.join(script_dir, "..", "Data", "situationCounts_432.csv")
situations_df = pd.read_csv(situations_path)


print("\n Type in inning number (1-9)")
inning_input = int(input())

print("\n Type in Top or Bot")
half_input = input().strip().lower()

if half_input in ("top", "t"):
    half_label = "Top"
elif half_input in ("bot", "bottom", "b"):
    half_label = "Bot"
else:
    raise ValueError(f"Unrecognized half-inning input: '{half_input}'. Use Top or Bot.")

if inning_input not in range(1, 10):
    raise ValueError(f"Inning must be 1-9, got {inning_input}.")


half_inning_df = situations_df[
    (situations_df["inning"] == inning_input)
    & (situations_df["inning_topbot"].astype(str) == half_label)
].copy()

if len(half_inning_df) != 24:
    raise ValueError(
        f"Expected 24 rows for inning {inning_input} {half_label}, "
        f"found {len(half_inning_df)}."
    )

base_order = ["000", "100", "010", "001", "110", "101", "011", "111"]

half_inning_df["base_state"] = (
    half_inning_df["1b"].astype(int).astype(str) +
    half_inning_df["2b"].astype(int).astype(str) +
    half_inning_df["3b"].astype(int).astype(str)
)
half_inning_df["base_state"] = pd.Categorical(
    half_inning_df["base_state"], categories=base_order, ordered=True
)

pct_table = half_inning_df.pivot_table(
    values="higher_re_after_pct",
    index="base_state",
    columns="outs_when_up",
    aggfunc="mean"
)

pct_table = pct_table.reindex(index=base_order, columns=[0, 1, 2])
pct_table.columns = ["0 outs", "1 out", "2 outs"]


colors = plt.cm.bwr(np.linspace(0, 1, 256))
colors[:, :3] = colors[:, :3] * 0.6 + 0.4
pastel_cmap = LinearSegmentedColormap.from_list("pastel_bwr", colors)


def format_bases_from_state(state):
    return (
        f"{'1B' if state[0] == '1' else '—'} "
        f"{'2B' if state[1] == '1' else '—'} "
        f"{'3B' if state[2] == '1' else '—'}"
    )


def plot_re_table(table, fig_title, subtitle=None, pct_format=False):
    row_labels = [format_bases_from_state(str(state)) for state in table.index]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axis("off")

    fmt = (lambda x: f"{x:.3%}" if not np.isnan(x) else "") if pct_format else (lambda x: f"{x:.3f}" if not np.isnan(x) else "")

    t = ax.table(
        cellText=[[fmt(x) for x in row] for row in table.values],
        rowLabels=row_labels,
        colLabels=table.columns,
        cellLoc="center",
        loc="center",
        bbox=[0.35, 0, 1, 1]
    )

    valid_values = table.values[~np.isnan(table.values)]
    norm = matplotlib.colors.TwoSlopeNorm(
        vmin=np.percentile(valid_values, 1),
        vcenter=np.percentile(valid_values, 50),
        vmax=np.percentile(valid_values, 99)
    )

    cells = t.get_celld()

    # setting widths
    for (row, col), cell in cells.items():
        if col == -1:
            cell.set_width(0.2)
        else:
            cell.set_width(0.15)

    # setting colors
    for (row, col), cell in cells.items():
        if row == 0:
            cell.set_facecolor("black")
            cell.set_text_props(color="white", weight="bold")
        elif col == -1:
            cell.set_facecolor("black")
            cell.set_text_props(color="white", weight="bold")
        else:
            actual_row = row - 1
            value = table.iloc[actual_row, col]
            if not np.isnan(value):
                color = pastel_cmap(norm(value))
                cell.set_facecolor(color)

    t.auto_set_font_size(False)
    t.set_fontsize(9)
    t.scale(1, 1.6)

    plt.suptitle(fig_title, fontsize=14, fontweight="bold", y=0.95)
    if subtitle:
        plt.figtext(0.5, 0.87, subtitle, fontsize=10, ha="center")
    plt.tight_layout(rect=[0, 0, 1, 0.88])


avg_pct = (
    half_inning_df["higher_re_after_count"].sum()
    / half_inning_df["situations_after_count"].sum()
)

plot_re_table(
    pct_table,
    fig_title=f"P(Higher RE After): {half_label} {inning_input}{'st' if inning_input == 1 else 'nd' if inning_input == 2 else 'rd' if inning_input == 3 else 'th'}",
    subtitle=f"Avg probability across all 24 states: {avg_pct:.3%}",
    pct_format=True
)

plt.show()