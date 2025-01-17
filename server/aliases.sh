alias shell='docker run -it --rm -e USER_ID=$(id -u) -e GROUP_ID=$(id -g) -v $(pwd)/app:/home/user/app bnetbutter/poetry-base:latest bash'

alias build_dev='docker build -f dev.dockerfile -t fooddist_devdocker .'
alias start_dev='docker run --env-file ../.env --network food-dist_default --name fooddist_dev_container -d -e USER_ID=$(id -u) -e GROUP_ID=$(id -g) -v $(pwd)/app:/home/user/app fooddist_devdocker'
alias shell_dev='docker exec --env-file ../.env --user user -it -w /home/user/app fooddist_dev_container poetry run bash'