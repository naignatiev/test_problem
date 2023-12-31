# CSVKeeper

## Install Linux
```shell
git clone https://github.com/naignatiev/test_problem.git
cd test_problem
python -m venv venv
pip install -r requirements.txt
flask run
```

## Install Docker
```shell
git clone https://github.com/naignatiev/test_problem.git
docker build -t test_problem .
docker run -d -p 5000:5000 --name test_problem_container test_problem
```
Можно также запустить cli скрипт, чтобы он наполнил базу данных
```shell
docker exec -it test_problem_container bash # если не в докере, пропустить
python cli_utils.py fill-database
```
## Методы
Я тестил в Postman, но скриншоты неудобно к README прикалывать, поэтому на питоне

### Добавление таблицы
```python
with open('data/testresources/data.csv', 'rb') as f:
    data = f.read()
requests.post('http://localhost:5000/api/dataset', data=data,
              headers={'File-Name': 'data.csv', 'Content-Type': 'text/csv'})
```

### Получение данных о табличках
```python
requests.get('http://localhost:5000/api/dataset')
```

### Получение данных таблицы
```python
requests.get('http://localhost:5000/api/content?dataset_id=1')
```
Фильтр можно указать любой в формате pandas экранируя специальные символы url (requests это делает сам)
```python
requests.get('http://localhost:5000/api/content', params={'dataset_id': 1, 'filter': 'A=="text"&B>0'})
```
Для сортировки нужно передать sort и order. В sort через запятую перечисление названий колонок, в order 'asc' или 'desc'
```python
requests.get(r'http://localhost:5000/api/content?dataset_id=1&sort=A,B&order=asc,desc')
```
