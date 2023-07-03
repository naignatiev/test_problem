from collections import namedtuple
from random import randint, gauss

from names import get_full_name

SklearnLikeDataset = namedtuple('SklearnLikeDataset', ['data', 'feature_names'])


def get_age() -> int:
    return randint(5, 100)


def get_height() -> float:
    return gauss(mu=170, sigma=20)


def get_weight() -> float:
    return gauss(mu=75, sigma=20)


def load_extra(dataset_length: int = 1000) -> SklearnLikeDataset:
    data = []
    for _ in range(dataset_length):
        data.append([
            get_full_name(),
            get_age(),
            get_height(),
            get_weight()
        ])
    return SklearnLikeDataset(
        data=data,
        feature_names=['full_name', 'age', 'height', 'weight']
    )
