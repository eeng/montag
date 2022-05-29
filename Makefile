test:
	poetry run pytest

test-watch:
	poetry run ptw

start:
	FLASK_APP=montag/web/app.py FLASK_ENV=development FLASK_SKIP_DOTENV=1 poetry run flask run

console:
	poetry run ipython
