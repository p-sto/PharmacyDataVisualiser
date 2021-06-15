"""Stores implementations of different functions"""
from typing import List, Dict, Tuple, Optional, cast

from pandas import DataFrame
import numpy as np

from dataVisualizer.data_containers.results_matrix import DataMatrix
from dataVisualizer.input_data_parser.parsers import SingleFileParser, DoubleFileParser, ParserABC

OUTPUT_EXCEL_FILE_NAME = 'ordered_data.xlsx'
OUTPUT_EXCEL_FILE_NAME_TRANSPOSED = 'ordered_data_transposed.xlsx'


def get_data_matrix(source_dir: str, data_fil_name: str, order_fil_name: Optional[str]) -> ParserABC:
    """Get input data as DataFrame with ordered data"""
    if order_fil_name:
        return cast(ParserABC, SingleFileParser(source_dir, data_fil_name, order_fil_name).get_result_matrix())
    return cast(ParserABC, DoubleFileParser(source_dir, data_fil_name).get_result_matrix())


def generate_output_excels(result_matrix: DataMatrix, output_dir: str) -> None:
    """Generate excel outputs"""
    result_matrix.data.to_excel('{}/{}'.format(output_dir, OUTPUT_EXCEL_FILE_NAME), index=False)
    result_matrix.transposed_data.to_excel('{}/{}'.format(output_dir, OUTPUT_EXCEL_FILE_NAME_TRANSPOSED))


def get_samples(data: DataFrame) -> Dict:
    """Return names of samples"""
    return data.to_dict()


def get_mean_and_std(data: List) -> Tuple[float, float]:
    """Calculate mean and std deviation for given data"""
    return float(np.mean(data)), float(np.std(data))


def filter_extreme_values(data: List[float], filter_sigma: float = 3) -> List[float]:
    """Calculate mean value and filter values greater than defined sigma value"""
    mean, _ = get_mean_and_std(data)
    return [x for x in data if mean - mean * filter_sigma < x < mean + mean * filter_sigma]
