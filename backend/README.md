# Absoluver Flask Backend

The backend flask app is an api that allows get requests with equation as params and send bank a json data with steps of solving the equation.

Move to the backend directory and run the following commands:

## Creating a virtual environment (Windows)

Initialiaze the environment folder:
```
$ virtualenv.exe venv
```

If virtualenv is not found run
```
$ pip install virtualenv.exe
```

Activate the virtual environment:
```
$ source venv/Scripts/activate
```

## Creating a virtual environment (MACOS)

Initialiaze the environment folder:
```
$ virtualenv venv
```

If virtualenv is not found run
```
$ pip install virtualenv
```

Activate the virtual environment:
```
$ source venv/bin/activate
```


## Installation of dependencies

Install dependancies with pip:

```
$ pip install -r requirements.txt
```



## Running the backend

Run the following command:

```
$ python main.py
```



## Flask Application Structure 
```
.
|──── main.py
|──── requirements.txt
|──── README.md



##Flask settings
DEBUG = True  # True/False
TESTING = False
