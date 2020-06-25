from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class CompoundData:
    name: str
    values: List[float]
    samples: List[str]

    def get_non_missing_values(self, prefix: str = '') -> List[float]:
        """Return non-zero values"""
        non_missing_values = []
        for sample, val in zip(self.samples, self.values):
            non_missing_values.append(val) if val != 1 and sample.lower().startswith(prefix) else non_missing_values.append(None)
        return non_missing_values

    def get_non_missing_samples(self, prefix: Optional[str] = None) -> List[str]:
        """Return samples for non-zero values"""
        non_missing_samples = []
        for sample, val in zip(self.samples, self.values):
            non_missing_samples.append(sample) if val != 1 and sample.lower().startswith(prefix) else non_missing_samples.append(None)
        return non_missing_samples

    @property
    def quality_values(self) -> List[Union[float, None]]:
        """"""
        return [val if sample.lower().startswith('qc') else None for sample, val in zip(self.samples, self.values)]

    @property
    def quality_samples(self) -> List[Union[float, None]]:
        """"""
        return [sample if sample.lower().startswith('qc') else None for sample in self.samples]

    def __repr__(self) -> str:
        return '{}: Samples: {}'.format(self.name, len(self.samples))