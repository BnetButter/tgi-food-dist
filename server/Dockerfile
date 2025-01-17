FROM bnetbutter/poetry-base:latest

WORKDIR /home/user/app

COPY ./app .

RUN poetry install --no-root

WORKDIR /home/user/app/fooddistserver

CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "fooddistserver.wsgi:application"]