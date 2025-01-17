FROM bnetbutter/poetry-base:latest

WORKDIR /home/user/app

COPY ./app .

RUN poetry install --no-root

WORKDIR /home/user/app/fooddistserver

# for system
RUN pip3 install mypy
RUN apt-get update && apt-get install -y postgresql-client
# Command to keep the container running


CMD ["tail", "-f", "/dev/null"]
