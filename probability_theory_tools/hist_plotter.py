import matplotlib.pyplot as plt


def hist_plot(distr):
    plt.clf()
    plt.hist(distr, bins=30, color="skyblue", edgecolor="black")

    plt.xlabel("Values", fontsize=14)
    plt.ylabel("Frequency", fontsize=12)
    plt.title("Basic Histogram", fontsize=12)
    plt.grid(axis="y", alpha=0.75)

    plt.show()
    # plt.savefig(fname, dpi=300, bbox_inches='tight')
