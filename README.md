# Yandex Backend School
>Чтобы немного скрасить жизнь людей на самоизоляции, вы решаете открыть
интернет-магазин по доставке конфет "Сласти от всех напастей".

Python REST API сервис, который позволяет нанимать курьеров на работу,
принимать заказы и оптимально распределять заказы между курьерами, попутно считая их рейтинг и заработок.

# Запуск

```console
$ waitress-serve --call 'candy_delivery:create_app'
```

# Тестирование

```console
$ pytest
```
# Установка

```console
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt install python3-pip
$ pip3 install wheel
$ sudo apt install git
$ git clone git@github.com:Mathless/backendschool.git
$ cd backendschool/
$ python3 -m pip install -r requirements.txt
$ sudo apt-get update
$ sudo apt install python-pytest
$ pip3 install flask
$ sudo apt install python3-flask
$ pip3 install backendschool-1.0-py3-none-any.whl
```
Когда все зависимости установлены, находясь в папке **backendschool**:
```console
$ export FLASK_APP=candy_delivery
$ flask init-db
$ waitress-serve --call 'candy_delivery:create_app'
```
# Зависимости

```python3
Package     Version

pytest~=6.2.2
Click~=7.0
Flask~=1.1.1
jsonschema~=3.2.0
MarkupSafe~=1.1.0
python-dateutil~=2.7.3
```
