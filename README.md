# Wolt Summer 2024 Engineering Internships

This project is `Delivery Fee Calculator` for [Wolt Software Engineering Internships](https://github.com/woltapp/engineering-internship-2024) implemented using Python. It calculates a delivery fee based on the cart value, the number of items in the cart, the time of the order, and the delivery distance.

API implementation is done using [FastAPI](https://fastapi.tiangolo.com/) framework and for Unit tests was used [Pytest](https://docs.pytest.org/en/8.0.x/) framework.

<br/>

## Development

### With Docker

#### Running the app

Run the app:
```bash
$> docker compose up
```

The API documentation is available in http://127.0.0.1:8000/docs.

#### Tests
```bash
$> docker compose run delivery-fee-api pytest
```

### Without Docker

#### Setting things up

It's recommened to use [virtual enviroment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/), as it allows to avoid installing Python packages globally which could break system tools or other projects.

```bash
$> python3 -m venv .venv/
```

Activate the virtual environment:

* Linux / MacOS:
	```bash
	$> source .venv/bin/activate
	```
* Windows (CMD):
	```bash
	$> .venv/Scripts/activate.bat
	```

* Windows (Powershell)
	```bash
	$> .venv/Scripts/Activate.ps1
	```

Install the dependencies
```bash
$> pip install -r requirements.txt
```

#### Running the app

Run the server (`--reload` automatically restarts the server when there are changes in the code):
```bash
$> uvicorn app.main:app --reload
```

The API documentation is available in http://127.0.0.1:8000/docs.

#### Tests
```bash
$> pytest test.py
```