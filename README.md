# flask-socketio-boilerplate
A boilerplate for Flask with Flask-SocketIO


## Environment

pip 22.2.2

python 3.9.7

### Setup Environment 

This document assumes pyenv is installed. 
To setup pyenv, look [here](https://github.com/pyenv/pyenv#installation)

1. Install python version 3.9.7 

```shell
pyenv install 3.9.7

```

2. Setup virtualenv 

```shell
# Setup virtualenv 
pyenv virtualenv 3.9.7 flask-socketio-boilerplate

# Activate created virtualenv 
pyenv activate flask-socketio-boilerplate

# To remove virtualenv use the following commands:
pyenv uninstall flask-socketio-boilerplate
pyenv virtualenv-delete 3.9.7/envs/flask-socketio-boilerplate

```

## Dependencies

[eventlet](http://eventlet.net/) is used as asynchronous service support.

Flask-SocketIO automatically selects eventlet when it is installed. Otherwise it will use Werkzeug. Look [here](https://flask-socketio.readthedocs.io/en/latest/intro.html) for more details.

## How to run


1. Install requirements first.

```shell
pip install -r requirements.txt
```

2. Run with python command. (Don't run with flask.)

```shell
python main.py
```

3. See results 

```
$ python main.py
2022-10-14 12:08:59,391 [INFO] initializing socketio
2022-10-14 12:08:59,391 [INFO]  * Restarting with stat
2022-10-14 12:08:59,526 [INFO] initializing socketio
2022-10-14 12:08:59,526 [WARNING]  * Debugger is active!
2022-10-14 12:08:59,532 [INFO]  * Debugger PIN: 122-632-373
(38065) wsgi starting up on http://127.0.0.1:5000
```
