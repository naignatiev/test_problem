from pathlib import Path


class Config:
    STORAGE_PATH = Path('data/')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    MAX_COLUMN_STR_LENGTH = 1000
    DATASET_PAGES_PER_REQUEST = 100
    DEFAULT_SEPARATOR = ','
    PORT = 5000
    TEMPLATES_AUTO_RELOAD = True
    ROWS_IN_REQUEST_COUNT = 200


class UIConfig:
    FILES_ON_PAGE = 5
