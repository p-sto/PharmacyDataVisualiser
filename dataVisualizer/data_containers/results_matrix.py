"""Stores implementations of input data parsers"""
from typing import List

import pandas as pd

from dataVisualizer.data_containers.compound import Compound
from dataVisualizer.exceptions import NotFound


class DataMatrix:
    """Represents Data Matrix"""

    def __init__(self, compounds: List[Compound], data: pd.DataFrame):
        """Initialize objects"""
        self.compounds = compounds
        self.data = data

    @property
    def transposed_data(self) -> pd.DataFrame:
        """Return transposed matrix"""
        return pd.DataFrame(self.data).transpose()

    def get_compound_by_name(self, name: str) -> Compound:
        """Return Compound based on name"""
        searched = [x for x in self.compounds if x.name == name]
        if not searched:
            raise NotFound('Provided Compound {} was not found.'.format(name))
        return searched[0]

    def get_compounds_names_list(self) -> List[str]:
        """Return list of Compounds names"""
        return [x.name for x in self.compounds]
