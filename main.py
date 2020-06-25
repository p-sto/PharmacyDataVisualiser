import os
from enum import Enum

from collections import OrderedDict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

from functions import read_xls_file, get_list_of_compounds, get_list_of_compound_data, calc_comp_data_average, \
    calc_comp_data_sum

sns.set()

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

RESOURCES_DIR = 'resources'
OUTPUTS = 'outputs'


class PatientGroups(Enum):
    """Represents patients data groups"""
    GROUP_1 = 'wnp'
    GROUP_2 = 'bezwnp'


if __name__ == '__main__':
    data_fil = read_xls_file('{}/{}'.format(RESOURCES_DIR, 'dane1.xls'))
    sample_order_fil = read_xls_file('{}/{}'.format(RESOURCES_DIR, 'order.xls'))

    order_list = list(sample_order_fil['order'])

    if not os.path.exists(OUTPUTS):
        os.mkdir(OUTPUTS)

    ordered_data = OrderedDict()
    ordered_data['Compound'] = get_list_of_compounds(data_fil)
    for sample in order_list:
        ordered_data[sample] = data_fil[sample].to_list()
    ordered_df = pd.DataFrame(ordered_data)
    compounds = get_list_of_compound_data(ordered_df)

    # embed()

    # calculate average value for every row, [1:] since first element in values will be 'compound'
    ordered_df['Average'] = [calc_comp_data_average(cmp) for cmp in compounds]
    ordered_df['SUM TUS'] = [calc_comp_data_sum(cmp) for cmp in compounds]

    transposed_ordered_df = pd.DataFrame(ordered_df).transpose()

    label = transposed_ordered_df[0].values[0]

    ordered_df.to_excel('ordered_data.xls', index=False)
    transposed_ordered_df.to_excel('ordered_data_transposed.xls')

    for cmp in compounds:
        logger.info('Working on %s', cmp.name)
        plt.figure(figsize=(14, 8))
        sns.set(style="darkgrid")

        ax = sns.regplot(x=list(range(len(cmp.get_non_missing_values(prefix='bezwnp')))),
                         y=cmp.get_non_missing_values(prefix='bezwnp'),
                         fit_reg=False)
        sns.regplot(x=list(range(len(cmp.get_non_missing_values(prefix='wnp')))),
                    y=cmp.get_non_missing_values(prefix='wnp'),
                    fit_reg=False,
                    marker='v')
        # mask points with red-dotted quality samples
        sns.regplot(x=range(len(cmp.quality_values)),
                    y=cmp.quality_values,
                    ci=None,
                    color='red',
                    truncate=False)

        ax.set(xlabel='Acquisition order', ylabel='Signal')
        ax.legend(labels=('regression', 'bezwnp', 'wnp', 'QC'),
                  loc='best')

        plt.title(cmp.name)
        plt.savefig('{}/{}.png'.format(OUTPUTS, cmp.name), bbox_inches='tight')
        plt.cla()
        plt.close()
    '%load_ext autoreload'
    '%autoreload'
