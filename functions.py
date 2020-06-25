from typing import List, Dict

from pandas import DataFrame
import pandas as pd

from compund_data import CompoundData


def validate_compound_data(data: CompoundData) -> CompoundData:
    """Validate CompoundData object"""
    assert len(data.values) == len(data.samples)
    return data


def read_xls_file(file_name: str) -> DataFrame:
    """Read data file"""
    assert file_name.endswith('xls'), 'Input data file must be xls file'
    return pd.read_excel(file_name)


def get_list_of_compounds(data: DataFrame) -> List:
    """Return list of compounds"""
    return data['Compound'].to_list()


def get_samples(data: DataFrame) -> Dict:
    """Return names of samples"""
    return data.to_dict()


def calc_comp_data_average(data: CompoundData, include_missing: bool = False) -> float:
    """Calculate average value"""
    if not include_missing:
        return sum([x for x in data.get_non_missing_values() if x]) / len([x for x in data.get_non_missing_values() if x])
    return sum(data.values) / len(data.values)


def calc_comp_data_sum(data: CompoundData) -> float:
    """Calculate average value"""
    return sum(data.values)


def get_list_of_compound_data(data: DataFrame) -> List[CompoundData]:
    """Return list of CompoundData objects"""
    return [validate_compound_data(CompoundData(comp[0], comp[1:], data.keys()[1:])) for comp in data.values]
