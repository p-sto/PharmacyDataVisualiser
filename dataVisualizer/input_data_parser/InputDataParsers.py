""""""
from abc import ABC
from collections import OrderedDict
from typing import List

from dataVisualizer.data_containers.ResultMatrix import ResultMatrix
from dataVisualizer.data_containers.compund_data import CompoundData

from pandas import DataFrame
import pandas as pd


def read_xls_file(file_name: str) -> DataFrame:
    """Read data file"""
    assert file_name.endswith('xls'), 'Input data file must be xls file'
    return pd.read_excel(file_name)


def get_list_of_compounds(data: DataFrame) -> List:
    """Return list of compounds"""
    return data['Compound'].to_list()


def calc_comp_data_average(data: CompoundData, include_missing: bool = False) -> float:
    """Calculate average value"""
    if not include_missing:
        return sum([x for x in data.get_non_missing_values() if x]) / len(
            [x for x in data.get_non_missing_values() if x])
    return sum(data.values) / len(data.values)


def calc_comp_data_sum(data: CompoundData) -> float:
    """Calculate average value"""
    return sum(data.values)


def validate_compound_data(data: CompoundData) -> CompoundData:
    """Validate CompoundData object"""
    assert len(data.values) == len(data.samples)
    return data


def get_list_of_compound_data(data: DataFrame) -> List[CompoundData]:
    """Return list of CompoundData objects"""
    return [validate_compound_data(CompoundData(comp[0], comp[1:], data.keys()[1:])) for comp in data.values]


class ParserABC(ABC):

    def parse(self) -> None:
        raise NotImplementedError

    def get_result_matrix(self) -> ResultMatrix:
        raise NotImplementedError


class SingleFileParser(ParserABC):
    """Parser for single input file"""

    def __init__(self, source_dir: str, data_file_name: str, order_fil_name: str):
        self.source_dir = source_dir
        self.data_file_name = data_file_name
        self.order_file_name = order_fil_name
        self._raw_parsed_data = None
        self._compounds = None

    def parse(self) -> None:
        data_fil = read_xls_file('{}/{}'.format(self.source_dir, self.data_file_name))
        sample_order_fil = read_xls_file('{}/{}'.format(self.source_dir, self.order_file_name))

        ordered_data = OrderedDict()
        ordered_data['Compound'] = get_list_of_compounds(data_fil)

        for sample in list(sample_order_fil['order']):
            ordered_data[sample] = data_fil[sample].to_list()
        self._raw_parsed_data = pd.DataFrame(ordered_data)
        self._compounds = get_list_of_compound_data(self._raw_parsed_data)

        # calculate average value for every row, [1:] since first element in values is always valued 'compound'
        self._raw_parsed_data['Average'] = [calc_comp_data_average(cmp) for cmp in self._compounds]
        self._raw_parsed_data['SUM TUS'] = [calc_comp_data_sum(cmp) for cmp in self._compounds]

    def get_result_matrix(self) -> ResultMatrix:
        self.parse()
        return ResultMatrix(self._compounds, self._raw_parsed_data)


class DoubleFileParser(ParserABC):
    """Parser for double input file"""

    def __init__(self, source_dir: str, data_fil_name: str):
        self.source_dir = source_dir
        self.data_fil_name = data_fil_name
        self._raw_parsed_data = None

    def parse(self) -> None:
        pass

    def get_result_matrix(self) -> ResultMatrix:
        self.parse()
        return ResultMatrix(self._compounds, self._raw_parsed_data)
