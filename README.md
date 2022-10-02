# Development guide

## Prequirements

Install required packages within virtual environment (equivalent to node_modules).

If it doesn't exist yet, create one:

```shell
$ python -m venv .venv
```

Remember to activate virtual evironment:

### Windows/cmd:

```shell
> .venv\Scripts\activate.bat
```

### Linux/bash:

```shell
$ source .venv/Scripts/activate
```

Install packages:

```shell
$ pip install -r requirements.txt
```

## Running

Start the webserver:

```shell
$ uvicorn main:app --reload
```