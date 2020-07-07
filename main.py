import os
from enum import Enum

from collections import OrderedDict
import pandas as pd
import logging

from dataVisualizer.charts.distribution_chart import generate_normal_distribution_chart
from dataVisualizer.charts.trend_chart import generate_trend_chart
from dataVisualizer.functions import read_xls_file, get_list_of_compounds, get_list_of_compound_data,\
    calc_comp_data_average, calc_comp_data_sum

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

RESOURCES_DIR = 'resources'
OUTPUT_DIR = 'outputs'


class PatientGroups(Enum):
    """Represents patients data groups"""
    GROUP_1 = 'wnp'
    GROUP_2 = 'bezwnp'


if __name__ == '__main__':
    data_fil = read_xls_file('{}/{}'.format(RESOURCES_DIR, 'dane1.xls'))
    sample_order_fil = read_xls_file('{}/{}'.format(RESOURCES_DIR, 'order.xls'))

    order_list = list(sample_order_fil['order'])

    plots_dirs_names = ['trends', 'normal_distributions']
    for dir_name in plots_dirs_names:
        full_path = '{}/{}'.format(OUTPUT_DIR, dir_name)
        if not os.path.exists(full_path):
            os.mkdir(full_path)

    ordered_data = OrderedDict()
    ordered_data['Compound'] = get_list_of_compounds(data_fil)
    for sample in order_list:
        ordered_data[sample] = data_fil[sample].to_list()
    ordered_df = pd.DataFrame(ordered_data)
    compounds = get_list_of_compound_data(ordered_df)

    # calculate average value for every row, [1:] since first element in values is always valued 'compound'
    ordered_df['Average'] = [calc_comp_data_average(cmp) for cmp in compounds]
    ordered_df['SUM TUS'] = [calc_comp_data_sum(cmp) for cmp in compounds]

    transposed_ordered_df = pd.DataFrame(ordered_df).transpose()
    ordered_df.to_excel('{}/{}'.format(OUTPUT_DIR, 'ordered_data.xls'), index=False)
    transposed_ordered_df.to_excel('{}/{}'.format(OUTPUT_DIR, 'ordered_data_transposed.xls'))

    for cmp in compounds:
        logger.info('Working on %s', cmp.name)
        generate_trend_chart(cmp, OUTPUT_DIR)
        generate_normal_distribution_chart(cmp, OUTPUT_DIR)
