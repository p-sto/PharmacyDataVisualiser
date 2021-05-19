"""Contains all functions related to generating distribution chart"""
import logging

import seaborn as sns
import matplotlib.pyplot as plt

from dataVisualizer.data_containers.compound import Compound
from dataVisualizer.functions import filter_extreme_values

logger = logging.getLogger()

BINS = 20


def generate_normal_distribution_chart(compound: Compound, output_directory: str) -> None:
    """Generate normal distribution chart for provided compound"""
    logger.info('\t * Generating normal distribution chart')

    fig = plt.figure(figsize=(20, 10))
    sns.set(style="darkgrid")

    vals_g1 = [x for x in compound.get_non_missing_values(prefix='wnp') if x]
    vals_g2 = [x for x in compound.get_non_missing_values(prefix='bezwnp') if x]

    vals_g1 = filter_extreme_values(vals_g1, filter_sigma=2)
    vals_g2 = filter_extreme_values(vals_g2, filter_sigma=2)

    right_axis = plt.twinx()

    sns.histplot(
        vals_g1,
        bins=BINS,
        ax=right_axis,
        color="g",
        shrink=.8,
        kde=True,
    )

    sns.histplot(
        vals_g2,
        bins=BINS,
        ax=right_axis,
        color="b",
        shrink=.8,
        kde=True,
    )

    sns.histplot(
        compound.quality_values,
        bins=BINS,
        kde=False,
        color='r',
    )

    fig.legend(labels=['wnp_KDE', 'bezwnp_KDE', 'QC'], loc='upper right')

    plt.title(compound.name)
    plt.savefig('{}/normal_distributions/{}.png'.format(output_directory, '_'.join(compound.name.split())),
                bbox_inches='tight')
    plt.cla()
    plt.close()
