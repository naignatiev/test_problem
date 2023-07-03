import requests

# TODO: use test flask_app


def test_api():
    # only with empty db
    with open('tests/testresources/data.csv', 'rb') as f:
        data = f.read()
    requests.post('http://localhost:5000/api/dataset', data=data,
                  headers={'File-Name': 'data.csv', 'Content-Type': 'text/csv'})

    response = requests.get('http://localhost:5000/api/dataset')
    assert response.json()['response'] == [{
        'columns': [{'pandas_dtype': 'object', 'title': 'A'}, {'pandas_dtype': 'int64', 'title': 'B'}],
        'filename': 'data.csv',
        'id': 1}
    ]

    assert requests.get('http://localhost:5000/api/content?dataset_id=1').json()['data'] == [
        ['text', 1],
        ['other', -1],
        ['text', -1],
        ['other', 1],
        ['text', 2],
        ['other', 1]
    ]

    response = requests.get('http://localhost:5000/api/content', params={'dataset_id': 1, 'filter': 'A=="text"&B>0'})
    assert response.json()['data'] == [
        ['text', 1],
        ['text', 2]
    ]

    response = requests.get(r'http://localhost:5000/api/content?dataset_id=1&sort=A,B&order=asc,desc')
    assert response.json()['data'] == [
        ['other', 1],
        ['other', 1],
        ['other', -1],
        ['text', 2],
        ['text', 1],
        ['text', -1]
    ]
