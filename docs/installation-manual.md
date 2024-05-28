---
title: Installation Manual
author:
  - Luís Pedro de Sousa Oliveira Góis, nº 2018280716
  - Marco Manuel Almeida e Silva, nº 2021211653
  - João Vítor Fraga Maia Alves, nº 2016122878
date: \today
---

# Installation Manual

## Before Setting up your environment

Make sure you have a `.env` file containing the secrets for the stack
deployment.

You can take `example.env` as an example and change the values.

We will provide 2 ways of running and deploying our software.

1. Setup of an Ubuntu VM
2. Setup of environment in your local machine
<!-- 3. Docker compose stack -->

## Ubuntu [Recommended]

### Requirements

- Operating System: [Ubuntu 24.04](https://ubuntu.com/download/desktop)
- Python version >= 3.12 and Python venv >= 3.12 to setup the python virtual
  environment
```sh
sudo apt install python3.12 python3.12-venv
```
- [Docker](https://docs.docker.com/engine/install/ubuntu/)
```sh
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
- [Optional] Make
```sh
sudo apt install make
```

### Stack Deployment

#### Makefile way

The `dev` rule defined in the `Makefile` will deploy:
- docker-compose:
  - postgres:latest
  - dpage/pgadmin4
- Python flask app

And will open all links in your browser.

```sh
make dev
```

Pressing Ctrl+c will stop the flask app, but the docker compose stack will still
be running, to stop:

```sh
sudo docker compose stop
```

#### Docker

```sh
sudo docker compose up -d
(. .env && venv/bin/flask --app src/app.py --env-file .env run --debug --host "$SERVER_HOST" --port "$SERVER_PORT" --with-threads)
sudo docker compose stop
```
