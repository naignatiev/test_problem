from flask.blueprints import Blueprint
from flask import request, jsonify
import pandas as pd

from config import Config
from procompliance_test.models import add_dataset, get_datasets_list, delete_dataset_by_id, get_df_content,\
    IncorrectFilterQuery, IncorrectSortQuery, IncorrectOrderType, get_dataset_info
from procompliance_test.utils import get_df_from_content_string

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/api/dataset', methods=['GET', 'POST', 'DELETE'])
def dataset():
    if request.method == 'GET':
        offset = request.args.get('offset', 0)
        print(request)
        # TODO: refactor validation
        error_code, message = validate_dataset_get_args()
        if error_code:
            return jsonify(message=message), error_code
        return jsonify(response=get_datasets_list(offset=offset, limit=Config.DATASET_PAGES_PER_REQUEST))

    if request.method == 'POST':
        sep = request.headers.get('Separator', Config.DEFAULT_SEPARATOR)
        decoded_body = request.data.decode().strip()
        # TODO: refactor validation
        error_code, message = validate_dataset_post_args(
            sep=sep,
            body=decoded_body
        )
        if error_code:
            return jsonify(message=message), error_code
        add_dataset(
            filename=request.headers['File-Name'],
            content=decoded_body,
            sep=request.headers.get('Separator', Config.DEFAULT_SEPARATOR)
        )
        return jsonify(success=True)

    if request.method == 'DELETE':
        if dataset_id := request.args.get('dataset_id'):
            delete_dataset_by_id(int(dataset_id))
            return jsonify(success=True)
        else:
            return jsonify(message='Please set "dataset_id"'), 400


# # TODO: Nones in types
@api_blueprint.route('/api/content', methods=['GET'])
def content():
    sort = request.args.get('sort')
    order = request.args.get('order')
    if (sort and not order) or (not sort and order):
        return jsonify(message='Pass sort and order arguments together'), 400
    try:
        dataset_id = int(request.args.get('dataset_id'))
        content_df = get_df_content(
            dataset_id=dataset_id,
            filter_query=request.args.get('filter'),
            sort=sort,
            order=order,
            offset=int(request.args.get('offset', 0)),
            count=Config.ROWS_IN_REQUEST_COUNT
        )
    except IncorrectFilterQuery:
        return jsonify(message='Incorrect filter query'), 400
    except IncorrectSortQuery:
        return jsonify(message='Incorrect sort query'), 400
    except IncorrectOrderType:
        return jsonify(message='Incorrect order type. Order type must be "asc" or "desc"'), 400
    dataset_info = get_dataset_info(dataset_id)
    return dataset_info | {'data': content_df.values.tolist()}


def validate_dataset_get_args():
    if not request.args.get('offset', '0').isdigit():
        return 400, 'offset arg must be an integer'
    return None, None


def validate_dataset_post_args(sep, body) -> (int, str):
    if not body:
        return 400, 'Http body is empty'
    file_name = request.headers.get('File-Name')
    if not file_name:
        # Пожалуйста, напишите мне, если знаете best practice,
        # для того чтобы указать имя файла избегая форм и custom headers
        return 400, 'Please specify "File-Name" header'
    if not file_name.endswith('.csv'):
        return 400, 'File name must end with .csv'
    if request.headers.get('Content-Type') != 'text/csv':
        return 415, 'Content-Type header should be \"text/csv\"'
    try:
        get_df_from_content_string(body, sep)
    except pd.errors.ParserError:
        return 400, 'Error during parse csv-file'
    return None, None
