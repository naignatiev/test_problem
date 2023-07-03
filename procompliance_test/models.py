from typing import TypedDict

import pandas as pd

from app import db
from config import Config
from procompliance_test.utils import get_dataset_path_by_id, get_columns_from_content, get_df_from_content_string,\
    get_dtype_from_pd_series


class DatasetInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    columns = db.relationship('Column', backref='dataset_info')


class Column(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(Config.MAX_COLUMN_STR_LENGTH))
    pandas_dtype = db.Column(db.String(10), nullable=False)
    dataset_info_id = db.Column(db.Integer, db.ForeignKey(DatasetInfo.id), nullable=False)


class ColumnJSONType(TypedDict):
    title: str
    pandas_dtype: str


class DatasetJSONType(TypedDict):
    id: int
    filename: str
    columns: list[ColumnJSONType]


def add_dataset(filename: str, content: str, sep: str):
    """ Insert dataset info into db and save content to file """
    dataset_info = DatasetInfo(filename=filename)
    content_df = get_df_from_content_string(content, sep)
    columns = []
    for column_name in get_columns_from_content(content, sep):
        columns.append(
            Column(
                title=column_name,
                dataset_info=dataset_info,
                pandas_dtype=get_dtype_from_pd_series(content_df[column_name]))
        )
    db.session.add(dataset_info)
    db.session.flush()
    content_df.to_csv(get_dataset_path_by_id(dataset_info.id), sep=sep)
    db.session.commit()
    db.session.add_all(columns)


def get_datasets_list(offset: int, limit: int) -> list[DatasetJSONType]:
    data = []
    for _dataset in DatasetInfo.query.offset(offset).limit(limit):
        data.append(get_dataset_info_dict(_dataset))
    return data


def get_dataset_info(dataset_id: int) -> DatasetJSONType:
    dataset_info = DatasetInfo.query.get(dataset_id)
    return get_dataset_info_dict(dataset_info)


def get_dataset_info_dict(dataset: DatasetInfo) -> DatasetJSONType:
    return {
        'id': dataset.id,
        'filename': dataset.filename,
        'columns': [{'title': column.title, 'pandas_dtype': column.pandas_dtype} for column in dataset.columns]
    }


def delete_dataset_by_id(dataset_id: int) -> None:
    DatasetInfo.query.filter(DatasetInfo.id == dataset_id).delete()
    db.session.commit()


class IncorrectFilterQuery(Exception):
    """ Raises if pd.DataFrame.query fails """


class IncorrectSortQuery(Exception):
    """ Raises if pd.DataFrame.sort_values fails """


class IncorrectOrderType(Exception):
    """ Raises if order is not in ['asc', 'desc'] """


def get_df_content(
        dataset_id: int,
        filter_query: str | None = None,
        sort: str | None = None,
        order: str | None = None,
        offset: int = 0,
        count: int = Config.DATASET_PAGES_PER_REQUEST
        ):
    dataset_path = get_dataset_path_by_id(dataset_id)
    print('DATASET_PATH: ', dataset_path)
    if filter_query or order and sort:
        dataset_df = pd.read_csv(dataset_path)
    else:
        dataset_df = pd.read_csv(dataset_path, skiprows=lambda x: x not in range(offset, offset + count))
    if filter_query:
        try:
            dataset_df = dataset_df.query(filter_query)
        except NotImplementedError as exc:
            raise IncorrectFilterQuery(str(exc))
    if sort and order:
        try:
            sort, order = parse_content_representation_args(sort, order)
            dataset_df = dataset_df.sort_values(by=sort, ascending=order)
        except KeyError as exc:
            raise IncorrectSortQuery(str(exc))
    return dataset_df[offset: offset + count]


def parse_content_representation_args(sort: str, order: str) -> (list[str], list[bool]):
    order_as_list = []
    for order_type in order.split(','):
        if order_type == 'asc':
            order_as_list.append(True)
        elif order_type == 'desc':
            order_as_list.append(False)
        else:
            raise IncorrectOrderType
    return sort.split(','), order_as_list
