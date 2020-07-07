import os
import logging

from dataVisualizer.charts.distribution_chart import generate_normal_distribution_chart
from dataVisualizer.charts.trend_chart import generate_trend_chart
from dataVisualizer.functions import get_input_data, generate_output_excels

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

RESOURCES_DIR = 'resources'
OUTPUT_DIR = 'outputs'


if __name__ == '__main__':
    input_data, ordered_dataframe = get_input_data(RESOURCES_DIR, 'dane1.xls', 'order.xls')

    plots_dirs_names = ['trends', 'normal_distributions']
    for dir_name in plots_dirs_names:
        full_path = '{}/{}'.format(OUTPUT_DIR, dir_name)
        if not os.path.exists(full_path):
            os.mkdir(full_path)

    generate_output_excels(ordered_dataframe, OUTPUT_DIR)

    for compound in input_data:
        logger.info('Working on %s', compound.name)
        generate_trend_chart(compound, OUTPUT_DIR)
        generate_normal_distribution_chart(compound, OUTPUT_DIR)
