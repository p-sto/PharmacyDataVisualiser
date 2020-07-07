"""Contains all functions related to generating distribution chart"""
import logging

import seaborn as sns
import matplotlib.pyplot as plt

from dataVisualizer.data_containers.compund_data import CompoundData
from dataVisualizer.functions import filter_extreme_values

logger = logging.getLogger()


def generate_normal_distribution_chart(compound: CompoundData, output_directory: str) -> None:
    """Generate normal distribution chart for provided compound"""
    logger.info('\t * Generating normal distribution chart')
    fig = plt.figure(figsize=(18, 8))
    sns.set(style="darkgrid")
    vals_g1 = [x for x in compound.get_non_missing_values(prefix='wnp') if x]
    vals_g2 = [x for x in compound.get_non_missing_values(prefix='bezwnp') if x]
    vals_g1 = filter_extreme_values(vals_g1, filter_sigma=2)
    vals_g2 = filter_extreme_values(vals_g2, filter_sigma=2)
    qc_vals = compound.quality_values
    bins = 20
    sns.distplot(vals_g1, kde=False, bins=bins)
    sns.distplot(vals_g2, kde=False, bins=bins)
    sns.distplot(qc_vals, kde=False, bins=bins)
    right_axis = plt.twinx()
    sns.distplot(vals_g1, hist=False, bins=bins, ax=right_axis,
                 kde_kws={"lw": 3},
                 hist_kws={"histtype": "step", "linewidth": 3, "alpha": 1, "color": "g"})
    sns.distplot(vals_g2, hist=False, bins=bins, ax=right_axis,
                 # kde_kws={"lw": 3, "label": "KDE", 'cumulative': True},
                 kde_kws={"lw": 3},
                 hist_kws={"histtype": "step", "linewidth": 3, "alpha": 1, "color": "g"})

    fig.legend(labels=['wnp_KDE', 'bezwnp_KDE', 'QC'], loc='upper right')
    plt.title(compound.name)
    plt.savefig('{}/normal_distributions/{}.png'.format(output_directory, '_'.join(compound.name.split())),
                bbox_inches='tight')
    plt.cla()
    plt.close()
