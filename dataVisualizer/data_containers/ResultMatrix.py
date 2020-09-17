"""Stores implementations of input data parsers"""
from typing import List

import pandas as pd

from dataVisualizer.data_containers.compund_data import CompoundData


class ResultMatrix:

    def __init__(self, compounds: List[CompoundData], data: pd.DataFrame):
        self.compounds = compounds
        self.data = data

    @property
    def transposed_data(self):
        return pd.DataFrame(self.data).transpose()
