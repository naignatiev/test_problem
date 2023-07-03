from flask import render_template, request
from flask.blueprints import Blueprint

from procompliance_test.models import get_datasets_list, DatasetInfo
from config import UIConfig


ui_blueprint = Blueprint('ui', 'ui', template_folder='procompliance_test/templates')


@ui_blueprint.route('/datasets')
def datasets():
    curr_page = int(request.args.get('page', 0))
    offset = (curr_page - 1) * UIConfig.FILES_ON_PAGE
    datasets_count = DatasetInfo.query.count()
    pages_n = int(datasets_count / UIConfig.FILES_ON_PAGE) + bool(datasets_count % UIConfig.FILES_ON_PAGE)
    return render_template('ui/datasets.html', curr_page=curr_page, pages_n=pages_n,
                           datasets=get_datasets_list(offset=offset, limit=UIConfig.FILES_ON_PAGE))


@ui_blueprint.route('/content')
def content():
    return render_template('ui/content.html')
