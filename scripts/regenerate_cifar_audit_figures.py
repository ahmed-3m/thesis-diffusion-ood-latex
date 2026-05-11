from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "images"
IMG.mkdir(parents=True, exist_ok=True)

plt.rcParams.update(
    {
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "legend.fontsize": 10,
        "figure.titlesize": 15,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(IMG / name, dpi=220, bbox_inches="tight")
    plt.close(fig)


def fig_val_auroc_seeds():
    seeds = ["42", "123", "456"]
    aurocs = np.array([99.11, 98.95, 99.04])
    mean = aurocs.mean()
    std = aurocs.std(ddof=1)

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    colors = ["#2563eb", "#0f766e", "#7c3aed"]
    bars = ax.bar(seeds, aurocs, color=colors, width=0.62)
    ax.axhline(mean, color="#111827", linestyle="--", linewidth=1.5, label=f"mean = {mean:.2f}%")
    ax.fill_between(
        [-0.5, 2.5],
        mean - std,
        mean + std,
        color="#cbd5e1",
        alpha=0.45,
        label=f"±1 std = {std:.2f} pp",
    )
    for bar, val in zip(bars, aurocs):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.03, f"{val:.2f}", ha="center", va="bottom")
    ax.set_ylim(98.7, 99.3)
    ax.set_ylabel("Validation AUROC (%)")
    ax.set_xlabel("Seed")
    ax.set_title("Final Selected CIFAR Model Across 3 Seeds ($\\lambda=0.02$, $K=50$)")
    ax.legend(loc="lower left", frameon=False)
    save(fig, "fig_val_auroc_seeds.png")


def fig_training_summary():
    seeds = ["42", "123", "456"]
    aurocs = np.array([98.73, 98.86, 98.87])
    epochs = np.array([19, 19, 19])

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.6))
    colors = ["#2563eb", "#0f766e", "#7c3aed"]

    bars = axes[0].bar(seeds, aurocs, color=colors, width=0.62)
    for bar, val in zip(bars, aurocs):
        axes[0].text(bar.get_x() + bar.get_width() / 2, val + 0.03, f"{val:.2f}", ha="center", va="bottom")
    axes[0].set_ylim(98.5, 99.0)
    axes[0].set_ylabel("Best validation AUROC (%)")
    axes[0].set_xlabel("Seed")
    axes[0].set_title("Ablation Checkpoint Performance")

    bars = axes[1].bar(seeds, epochs, color=colors, width=0.62)
    for bar, val in zip(bars, epochs):
        axes[1].text(bar.get_x() + bar.get_width() / 2, val + 0.4, f"{val}", ha="center", va="bottom")
    axes[1].set_ylim(0, 24)
    axes[1].set_ylabel("Best epoch")
    axes[1].set_xlabel("Seed")
    axes[1].set_title("Checkpoint Selection Epoch")

    fig.suptitle("Retained 3-Seed Ablation Checkpoint Summary ($\\lambda=0.01$)")
    save(fig, "fig_training_summary.png")


def fig_lambda_sweep():
    lambdas = ["0.0", "0.001", "0.01", "0.02", "0.05", "0.1"]
    within = np.array([92.52, 97.32, 98.82, 99.03, 98.51, 96.67])
    within_std = np.array([11.07, 0.0, 0.06, 0.07, 0.0, 0.0])
    svhn = np.array([100.0, 92.0, 90.5, 96.6, 97.3, 86.9])
    epochs = np.array([79, 19, 19, 29, 19, 149])
    x = np.arange(len(lambdas))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8))

    ax1.plot(x, within, marker="o", color="#2563eb", linewidth=2, label="Within-CIFAR")
    ax1.errorbar(x[[0, 2, 3]], within[[0, 2, 3]], yerr=within_std[[0, 2, 3]], fmt="none", ecolor="#2563eb", capsize=4)
    ax1.plot(x, svhn, marker="s", color="#b45309", linewidth=2, label="SVHN")
    ax1.scatter(x[[0, 5]], svhn[[0, 5]], color="#b45309", s=45, edgecolors="black", linewidths=0.5, zorder=3)
    ax1.annotate(
        "+6.5 pp",
        xy=(3, within[3]),
        xytext=(1.7, 93.8),
        arrowprops={"arrowstyle": "->", "lw": 1.2, "color": "#111827"},
        fontsize=10,
    )
    ax1.set_xticks(x, lambdas)
    ax1.set_ylim(85, 101)
    ax1.set_xlabel("$\\lambda$")
    ax1.set_ylabel("AUROC (%)")
    ax1.set_title("Audited AUROC by Separation-Loss Weight")
    ax1.legend(loc="lower left", frameon=False)

    ax2.bar(x, epochs, color=["#94a3b8", "#94a3b8", "#2563eb", "#16a34a", "#94a3b8", "#dc2626"], width=0.62)
    for xi, val in zip(x, epochs):
        ax2.text(xi, val + 2, f"{val}", ha="center", va="bottom", fontsize=10)
    ax2.set_xticks(x, lambdas)
    ax2.set_ylim(0, 165)
    ax2.set_xlabel("$\\lambda$")
    ax2.set_ylabel("Best epoch (seed 42)")
    ax2.set_title("Convergence Speed")

    save(fig, "fig_lambda_sweep.png")


def fig_cross_domain():
    labels = ["CIFAR-10\nwithin split", "Inkjet QC\n5-fold CV"]
    baseline = np.array([92.52, 86.73])
    best = np.array([99.03, 86.70])
    baseline_err = np.array([11.07, 2.30])
    best_err = np.array([0.07, 2.56])

    x = np.arange(len(labels))
    width = 0.34

    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    ax.bar(x - width / 2, baseline, width, yerr=baseline_err, capsize=4, color="#94a3b8", label="Baseline ($\\lambda=0$)")
    ax.bar(x + width / 2, best, width, yerr=best_err, capsize=4, color="#2563eb", label="Best retained setting")
    for xi, base, top in zip(x, baseline, best):
        delta = top - base
        ax.text(xi, max(base, top) + 2.4, f"{delta:+.2f} pp", ha="center", va="bottom")
    ax.set_xticks(x, labels)
    ax.set_ylabel("AUROC (%)")
    ax.set_ylim(75, 105)
    ax.set_title("Cross-Domain Effect of Separation Loss")
    ax.legend(frameon=False, loc="upper right")
    save(fig, "fig_cross_domain_comparison.png")


if __name__ == "__main__":
    fig_val_auroc_seeds()
    fig_training_summary()
    fig_lambda_sweep()
    fig_cross_domain()
    print("Regenerated audited CIFAR/inkjet figure assets.")
