# VitalVue

---
title: Relatório Base de dados
author:
  - João Vítor Fraga Maia Alves, nº 2016122878
  - Luís Pedro de Sousa Oliveira Góis, nº 2018280716
  - Marco Manuel Almeida e Silva, nº 2021211653
date: \today
---

## Brief Description

This project involves developing a Hospital Management System (HMS) that will
streamline hospital operations by managing patient care, scheduling, billing,
and resource allocation. The system will include functionalities for patients,
doctors, nurses, and assistants, with each having specific attributes and roles.
It will manage appointments, hospitalizations, surgeries, prescriptions, side
effects, and billing, with concurrency issues and triggers considered. Doctors
will have specializations organized hierarchically. any necessary database
schema details that are not explicitly defined should be determined.

## Definition

### Transaction / Potential concurrency conflicts

- When creating an appointment or surgery, we need to verify that the doctor and
  the nurses assigned are available in the date and time of the
  appointment/surgery.  For that we have to verify that there isn't an
  appointment/surgery with the same doctors and nurses already created in the
  same time block.
- Once we add a surgery to a hospitalization, we must create a bill for the
  hospitalization if it has not been created yet or update the hospitalization
  bill, adding the cost of the surgery to the bill.
- When adding a new surgery to the hospitalization, we must make sure there is
  not a surgery already added to the same date and time block.
- When scheduling an appointment for the patient, there cannot be an appointment
  already scheduled in the same date and time block.

## Development plan

### Planned Tasks

1. Database design and implementation: Define the database schema and set up the
   necessary tables.
2. Backend development: Write the necessary Python code to handle operations for
   the database, and create RESTful endpoints for communication with the frontend.
3. API testing using Postman: Test the RESTful endpoints to ensure they are
   accessible and return the expected results.
4. Documentation: Prepare documentation for installation, usage, and maintenance
   of the system for future reference.

### Initial Work Division per Team Member

1. Database design and implementation
2. Backend development
3. API testing using Postman
4. Documentation

### Timeline

1. Database design and implementation: Weeks 1-2
2. Backend development: Weeks 3-6
3. API testing using Postman and Documentation: Weeks 7-8

## ER Diagram

![ER Diagram](/assets/conceptual-diagram.png)

## Relational data model

![Relational Data Model](/assets/physical-diagram.png)

## Installation Manual

### Before Setting up your environment

Make sure you have a `.env` file containing the secrets for the stack
deployment.

You can take `example.env` as an example and change the values.

We will provide 2 ways of running and deploying our software.

1. Setup of an Ubuntu VM
2. Setup of environment in your local machine
<!-- 3. Docker compose stack -->

### Ubuntu [Recommended]

#### Requirements

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

#### Stack Deployment

##### Makefile way

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

##### Docker

```sh
sudo docker compose up -d
(. .env && venv/bin/flask --app src/app.py --env-file .env run --debug --host "$SERVER_HOST" --port "$SERVER_PORT" --with-threads)
sudo docker compose stop
```

## User Manual

### Getting Started

1. Download Postman
2. Open Postman and go to workspace
3. Import collection files found in: `VitalVue/postman/`

### Running Collections

With the collections imported you can run them seperately in order or out of order. This is the recommended order:

1. Vital Vue Register
- Registers one user of each type.
2. Vital Vue Appointments
- Schedules an appointments and sees the appointments for a patient.
3. Vital Vue Surgeries
- Schedules a surgery for a patient.
4. Vital Vue Prescriptions
- Adds prescriptions and gets the prescriptions for a patient.
5. Vital Vue Stats

You can run the collection by `right clicking` on them and selecting `Run collection`. It's recommended to tick `Persist responses for a session`, so that you can see the responses for each request.

### Requests

There is also the option to create new requests if needed. This is how each of them can be implemented.

#### Register Patient

##### Body Example

```json
{
    "username": "patient name",
    "email": "patient@email.com",
    "password": "123",
    "name": "Marco Silva"
}
```

##### Response

Responds with the status code and the new Vital Vue User ID.

#### Register Assistant

##### Body Example

```json
{
    "username": "assistant name",
    "email": "assistant@mail.com",
    "password": "123",
    "contract_details": "the best assistant",
    "name": "Alexandra"
}
```

##### Response

Responds with the status code and the new Vital Vue User ID.

#### Register Nurse

##### Body Example

```json
{
    "username": "nurse name",
    "email": "nurse@mail.com",
    "password": "123",
    "contract_details": "the best nurse",
    "name": "Alexandra",
    "category": "nurse category"
}
```

##### Response

Responds with the status code and the new Vital Vue User ID.

#### Register Doctor

##### Body Example

```json
{
    "username": "doctor name",
    "email": "doctor@mail.com",
    "password": "123",
    "contract_details": "the best doctor",
    "name": "Marco Silva",
    "license": "ortho"
}
```

##### Response

Responds with the status code and the new Vital Vue User ID.

#### User Authentication

##### Body Example

```json
{
    "username": "msilva2",
    "password": "123"
}
```

##### Response

Responds with the status code and the authorization token. This token will be automatically used in the remaining requests.

#### Schedule Appointment

##### Body Example

```json
{
    "doctor_id": 4,
    "date": "2024-10-23",
    "start_time": "17:30",
    "end_time": "18:00",
    "cost": 100
}
```

##### Response

Responds with the status code and the ID of the new appointment. 

#### See Appointments

Responds with the status code and the information about the appointments.

##### Response Example

```json
{
    "results": [
        {
            "date": "Wed, 23 Oct 2024 00:00:00 GMT",
            "doctor_id": 4,
            "id": 1
        },
        {
            "date": "Wed, 23 Oct 2024 00:00:00 GMT",
            "doctor_id": 4,
            "id": 2
        }
    ],
    "status": 200
}
```

#### Schedule Surgery

##### Body Example

```json
{
    "patient_user_id": 1,
    "doctor_user_id": 4,
    "nurses": [
        [3, "role1"],
        [3, "role2"],
        [3, "role3"]
    ],
    "date": "2024-05-24",
    "start_time": "15:30",
    "end_time": "16:00"
}
```

#### Get Prescriptions

Responds with the status code and the information about the patient prescriptions.

##### Response Example

```json
{
    "results": [
        {
            "id": 1,
            "posology": [
                {
                    "dose": 100,
                    "frequency": 2,
                    "medicine": "ben-u-ron"
                },
                {
                    "dose": 100,
                    "frequency": 2,
                    "medicine": "aspirin"
                }
            ],
            "validity": "Mon, 27 May 2024 00:00:00 GMT"
        },
        {
            "id": 2,
            "posology": [
                {
                    "dose": 100,
                    "frequency": 2,
                    "medicine": "ben-u-ron"
                }
            ],
            "validity": "Mon, 27 May 2024 00:00:00 GMT"
        }
    ],
    "status": 200
}
```

#### Add Prescription

##### Body Example

```json
{
    "type": "appointment",
    "event_id": 2,
    "validity": "2024-05-27",
    "medicines": [
        {"medicine": "ben-u-ron", "posology_dose": 100, "posology_frequency": 2},
        {"medicine": "aspirin", "posology_dose": 100, "posology_frequency": 2}
    ]
}
```

##### Response

Responds with the status code and the prescription ID.

#### Generate Monthly Report

Responds with the status code and the montly report.

##### Response Example

```json
{
    "results": [
        {
            "doctor": "Marco Silva",
            "month": "5",
            "surgeries": 4
        }
    ],
    "status": 200
}
```

## Contribution

1. Marco Manuel Almeida e Silva (42h)
  - Sql Queries
  - Python Code
  - Postman Collections
2. Luís Pedro de Sousa Oliveira Góis (38h)
  - Sql Queries
  - Python Code
  - Environment/Stack Setup (Docker, ...)
3. João Vítor Fraga Maia Alves (5h30m)
  - Presentation

## Attachments

The onda project saved as json are saved under the assets directory, among all
the figures as well.
