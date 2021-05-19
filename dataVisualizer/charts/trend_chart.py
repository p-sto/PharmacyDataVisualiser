"""Contains functionalities related to trend chart"""
import logging

import seaborn as sns
import matplotlib.pyplot as plt

from dataVisualizer.data_containers.compound import Compound

logger = logging.getLogger()


def generate_trend_chart(compound: Compound, output_directory: str):
    """Generate trend chart based on passed parameters"""
    logger.info('\t * Generating trend chart')
    plt.figure(figsize=(14, 8))
    sns.set(style="darkgrid")

    ax = sns.regplot(x=list(range(len(compound.get_non_missing_values(prefix='bezwnp')))),
                     y=compound.get_non_missing_values(prefix='bezwnp'),
                     fit_reg=False)
    sns.regplot(x=list(range(len(compound.get_non_missing_values(prefix='wnp')))),
                y=compound.get_non_missing_values(prefix='wnp'),
                fit_reg=False,
                marker='v')
    # mask points with red-dotted quality samples
    sns.regplot(x=list(range(len(compound.quality_values))),
                y=compound.quality_values,
                ci=None,
                color='red',
                truncate=False)

    ax.set(xlabel='Acquisition order', ylabel='Signal')
    ax.legend(labels=('regression', 'bezwnp', 'wnp', 'QC'), loc='best')

    plt.title(compound.name)
    save_directory = '{}/trends/{}.png'.format(output_directory, '_'.join(compound.name.split()))
    plt.savefig(save_directory, bbox_inches='tight')
    plt.cla()
    plt.close()
