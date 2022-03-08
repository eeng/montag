test:
	poetry run pytest

test-watch:
	poetry run ptw

start:
	FLASK_APP=montag/api/app.py FLASK_ENV=development poetry run flask run