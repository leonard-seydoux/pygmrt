import os
import matplotlib.pyplot as plt

python_logo_colors = {
    "blue": "#4B8BBE",
    "yellow": "#FFE873",
    "dark_blue": "#306998",
    "dark_yellow": "#FFD43B",
    "gray": "#646464",
    "light_gray": "#9B9B9B",
}

LINEWIDTH = 2

plt.rcParams["savefig.dpi"] = 300


def main():
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(3, 3))

    # Draw square
    square = plt.Rectangle(
        (0, 0),
        1,
        1,
        facecolor=python_logo_colors["light_gray"],
        linewidth=LINEWIDTH,
        edgecolor="k",
    )
    ax.add_patch(square)

    # Divide square lower left, and redot it 4 times
    ax.plot([0.5, 0.5], [0, 1], color="k", linewidth=LINEWIDTH)
    ax.plot([0, 1], [0.5, 0.5], color="k", linewidth=LINEWIDTH)
    ax.plot([0.25, 0.25], [0, 0.5], color="k", linewidth=LINEWIDTH)
    ax.plot([0, 0.5], [0.25, 0.25], color="k", linewidth=LINEWIDTH)
    ax.plot([0.125, 0.125], [0, 0.25], color="k", linewidth=LINEWIDTH)
    ax.plot([0, 0.25], [0.125, 0.125], color="k", linewidth=LINEWIDTH)
    ax.plot([0.0625, 0.0625], [0, 0.125], color="k", linewidth=LINEWIDTH)
    ax.plot([0, 0.125], [0.0625, 0.0625], color="k", linewidth=LINEWIDTH)

    # Color top right squares in blue
    for x in [0.5, 0.25, 0.125, 0.0625]:
        ax.add_patch(
            plt.Rectangle(
                (x, x),
                x,
                x,
                facecolor=python_logo_colors["blue"],
                linewidth=LINEWIDTH,
                edgecolor="k",
            )
        )

    for i, x in enumerate([0.5, 0.25, 0.125, 0.0625]):
        if i % 2 == 0:
            ax.add_patch(
                plt.Rectangle(
                    (x, 0),
                    x,
                    x,
                    facecolor=python_logo_colors["yellow"],
                    linewidth=LINEWIDTH,
                    edgecolor="k",
                )
            )
        else:
            ax.add_patch(
                plt.Rectangle(
                    (0, x),
                    x,
                    x,
                    facecolor=python_logo_colors["yellow"],
                    linewidth=LINEWIDTH,
                    edgecolor="k",
                )
            )

    # Remove axes
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    ax.axis("off")

    # Ensure images directory exists
    images_dir = os.path.join(os.path.dirname(__file__), "images")
    os.makedirs(images_dir, exist_ok=True)

    # Save
    logo_path = os.path.join(images_dir, "logo.png")
    fig.savefig(logo_path, transparent=True, bbox_inches="tight", pad_inches=0)
    print(f"✓ Logo saved to {logo_path}")


if __name__ == "__main__":
    main()
