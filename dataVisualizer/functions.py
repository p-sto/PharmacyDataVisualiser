from typing import List, Dict, Tuple, Optional

from pandas import DataFrame
import numpy as np

from dataVisualizer.data_containers import ResultMatrix
from dataVisualizer.input_data_parser.InputDataParsers import SingleFileParser, DoubleFileParser


def get_data_matrix(source_dir: str, data_fil_name: str, order_fil_name: Optional[str]) -> ResultMatrix:
    """Get input data as DataFrame with ordered data"""
    if order_fil_name:
        return SingleFileParser(source_dir, data_fil_name, order_fil_name).get_result_matrix()
    return DoubleFileParser(source_dir, data_fil_name).get_result_matrix()


def generate_output_excels(result_matrix: ResultMatrix, output_dir: str) -> None:
    """Generate excel outputs"""
    result_matrix.data.to_excel('{}/{}'.format(output_dir, 'ordered_data.xls'), index=False)
    result_matrix.transposed_data.to_excel('{}/{}'.format(output_dir, 'ordered_data_transposed.xls'))


def get_samples(data: DataFrame) -> Dict:
    """Return names of samples"""
    return data.to_dict()


def get_mean_and_std(data: List) -> Tuple[float, float]:
    """Calculate mean and std deviation for given data"""
    return np.mean(data), np.std(data)


def filter_extreme_values(data: List[float], filter_sigma: float = 3) -> List[float]:
    """Calculate mean value and filter values greater than defined sigma value"""
    mean, _ = get_mean_and_std(data)
    return [x for x in data if mean - mean * filter_sigma < x < mean + mean * filter_sigma]
