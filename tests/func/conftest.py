from pathlib import Path

import pandas as pd
import pytest
from mock import patch

from app import db
from app import app as flask_app
from extra_datasets import load_extra


# @pytest.fixture(scope='session', autouse=True)
# def flask_client():
#     with flask_app.test_client() as client:
#         with flask_app.app_context():
#             yield client
#
#
# @pytest.fixture(scope='session', autouse=True)
# def add_data(flask_client):
#     dataset = load_extra()
#     body = pd.DataFrame(dataset.data, columns=dataset.feature_names).to_string()
#     flask_client.post('/api/dataset', headers={'File-Name': 'test.csv', 'Content-Type': 'text/csv'},
#                       data=body)
