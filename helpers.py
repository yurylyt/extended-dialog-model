import numpy as np
np.set_printoptions(linewidth=2000, precision=3, suppress=True, formatter={'float': '{: 0.3f}'.format})

# check if .output dir exists, create if it doesn't
import os
if not os.path.exists('.output'):
    os.makedirs('.output')

def print_transition_matrix(matrix):
    print("\t\t| (1,1)\t| (1,2)\t| (1,3)\t| (2,1)\t| (2,2)\t| (2,3)\t| (3,1)\t| (3,2)\t| (3,3)")
    for i in range(9):
        print('---------------------------------------------------------------------------------')
        a = i // 3 + 1
        b = i % 3 + 1
        print(f'({a},{b})', '\t|', '\t| '.join(f'{x:.3f}'.rstrip('0').rstrip('.').rjust(4) for x in matrix[i]))

def _plot_results(results, plt):
    from matplotlib.ticker import MaxNLocator
    # rearrange results so that option 2 and 3 are swapped
    results = np.array(results)
    results[:, [1, 2]] = results[:, [2, 1]]
    labels = [r'$v_A$', r'$v_{alt}$', r'$v_B$']
    # labels = ['v_A', 'v_B', 'v_alt']

    cumsum = np.cumsum(results, axis=1)


    x = np.arange(cumsum.shape[0])
    # plt.plot(cumsum)

    hatch_patterns = ['/', '.', '\\']
    grayscale_colors = ['0.4', '0.95', '0.6']  # Shades of gray

    plt.grid(alpha=0.2, which='major', linestyle='-')
    for i in range(3):
        baseline = 0 if i == 0 else cumsum[:, i-1]
        plt.fill_between(x, baseline, cumsum[:, i], label=labels[i], alpha=0.8, color=grayscale_colors[i], hatch=hatch_patterns[i])

    # plt.xticks(ticks=x, labels=[f'{i}' for i in x])
    plt.set_xticks(ticks=x, labels=[f'{i}' for i in x])

    legend = plt.legend(fontsize=14)

    # Add border to legend items
    for legend_item in legend.legendHandles:
        legend_item.set_edgecolor('black')
    plt.set_ylim(bottom=0, top=1.0)
    plt.set_yticks(np.arange(0, 1.1, 0.1))
    # plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=10))
    plt.yaxis.set_major_locator(MaxNLocator(nbins=10))


def plot_side_by_side(results_a, results_b, name):
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

    ax1.set_title("Alice", fontsize=20)
    ax2.set_title("Bob", fontsize=20)
    ax2.set_xlabel("Dialog Iterations", fontsize=14)

    _plot_results(results_a, ax1)
    _plot_results(results_b, ax2)
    plt.savefig(f'.output/{name}.png', bbox_inches='tight')
    plt.show()

def plot_one(results, name):
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10, 5))
    ax1 = fig.add_subplot(111)

    ax1.set_title("Alice", fontsize=20)
    ax1.set_xlabel("Dialog Iterations", fontsize=14)

    _plot_results(results, ax1)
    plt.savefig(f'.output/{name}.png', bbox_inches='tight')
    plt.show()