import io
from pathlib import Path
from typing import Iterator

import pandas as pd

from config import Config


def get_dataset_path_by_id(dataset_id: int) -> Path:
    return Config.STORAGE_PATH / f"{dataset_id}.csv"


def get_columns_from_content(content: str, sep: str) -> Iterator[str]:
    """ Parse first row in csv file and iterate over columns """
    for i, column_name in enumerate(content.split('\n')[0].split(sep)):
        if i == 0 and column_name == '':
            yield 'Unnamed: 0'
        else:
            yield column_name


def get_df_from_content_string(content: str, sep: str) -> pd.DataFrame:
    return pd.read_csv(io.StringIO(content), sep=sep)


def get_dtype_from_pd_series(series: pd.Series) -> str:
    return str(series.dtype)
