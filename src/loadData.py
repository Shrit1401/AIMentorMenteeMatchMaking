from pathlib import Path
from typing import Tuple, Union

import pandas as pd


def loadMentees(path: Union[str, Path] = "data/mentees.csv") -> pd.DataFrame:
    return pd.read_csv(Path(path))


def loadMentors(path: Union[str, Path] = "data/mentors.csv") -> pd.DataFrame:
    return pd.read_csv(Path(path))


def loadData() -> Tuple[pd.DataFrame, pd.DataFrame]:
    mentees = loadMentees()
    mentors = loadMentors()
    return mentees, mentors
