# CSVKeeper

## Install Linux
```shell
git clone https://github.com/naignatiev/test_problem.git
python -m venv venv
pip install -r requirements.text
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
with open('data.csv', 'rb') as f:
    data = f.read()
requests.post('localhost:5000/api/dataset', data=data,
              headers={'File-Name': 'data.csv', 'Content-Type': 'text/csv'})
```

### Получение данных о табличках
```python
requests.get('localhost:5000/api/dataset')
```

### Удаление
```python
requests.delete('localhost:5000/api/dataset?dataset_id=1')
```

### Получение данных таблицы
```python
requests.get('localhost:5000/content?dataset_id=1')
```
Фильтр можно указать любой в формате pandas
```python
requests.get('localhost:5000/content?dataset_id=1&filter=A=="text"&B>0')
```
Для сортировки нужно передать sort и order. В sort через запятую перечисление названий колонок, в order 'asc' или 'desc'
```python
requests.get('localhost:5000/content?sort=A,B&order=asc,desc')
```

## Комментарии
* Много чего не сделал из того что хотел, не рассчитал время, которое отвёл себе для решения тестового
* Тестами не успел покрыть, оставил только те которые я писал чтобы что-то затестить в процессе
* Хотел сделать UI, но успел только страничку со списком /datasets 
* Пожалуйста, если тестовое реджект, напишите мне на почту комментарии по заданию: naignatiev@yandex.ru
* Я сделал offset, так что без него API возвращает по 100 записей на api/dataset и по 200 на api/content
