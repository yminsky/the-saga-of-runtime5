#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import os
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate space overhead plots.')
parser.add_argument('output_dir', type=str, help='Directory where output PNG files will be saved')
args = parser.parse_args()

# Create the output directory if it doesn't exist
os.makedirs(args.output_dir, exist_ok=True)

execs = { "rt4": "p4", "rt5": "p5", "up4": "u4", "up52": "u52", "new": "pq" }
modes = { "bytes": "bytes", "bigarrays":"ba", "lists": "lists"}
data = { (e, m): np.genfromtxt('results_' + execs[e] + '_' + modes[m] + '.txt') for e in execs for m in modes}

markers = {'bytes': '+', 'bigarrays': 'o', 'lists': '^'}
colors = {'new': 'blue', 'rt4': 'orange', 'rt5': 'green', 'up4': 'yellow', 'up52': 'red'}

series_order = ['rt4', 'up52', 'rt5', 'new']

region = (0,550)
plt.figure(figsize=(10,10))

# Increase font sizes
plt.rcParams.update({
    'font.size': 14,
    'axes.titlesize': 20,
    'axes.labelsize': 16,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14
})

plt.title("Requested vs Measured space_overhead", fontsize=20, pad=20)
plt.xlabel("Requested", fontsize=20, labelpad=15)
plt.ylabel("Measured", fontsize=20, labelpad=15)
plt.xlim(region)
plt.ylim(region)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.plot(range(10,600,10), range(10,600,10), color='black', label='ideal')

# Save the initial plot
filename = os.path.join(args.output_dir, f"space_overhead_0.png")
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"Saved plot to {os.path.abspath(filename)}")

# Add each series in order and save the plot
for i, e in enumerate(series_order, start=1):
    for (exec_name, m), d in data.items():
        if exec_name == e and len(d) > 0:
            plt.plot(d[:,0], d[:,1],
                     marker=markers[m],
                     color=colors[exec_name],
                     label=exec_name + "_" + m,
                     linewidth=1,
                     markersize=5)
    plt.legend(fontsize=14)

    # Save the figure as a PNG file
    filename = os.path.join(args.output_dir, f"space_overhead_{i}.png")
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Saved plot to {os.path.abspath(filename)}")
