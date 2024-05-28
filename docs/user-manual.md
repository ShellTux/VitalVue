---
title: User Manual
author:
  - Luís Pedro de Sousa Oliveira Góis, nº 2018280716
  - Marco Manuel Almeida e Silva, nº 2021211653
  - João Vítor Fraga Maia Alves, nº 2016122878
date: \today
---

# User Manual

## Getting Started

1. Download Postman
2. Open Postman and go to workspace
3. Import collection files found in: `VitalVue/postman/`

## Running Collections

With the collections imported you can run them seperately in order or out of order. This is the recommended order:

1. Vital Vue Register
2. Vital Vue Appointments
3. Vital Vue Surgeries
4. Vital Vue Prescriptions
5. Vital Vue Stats

You can run the collection by `right clicking` on them and selecting `Run collection`.
> [!NOTE]
> It's recommended to tick `Persist responses for a session`, so that you can see the responses for each request.

## Requests

### Register Patient

#### Body Example

```json
{
    "username": "patient name",
    "email": "patient@email.com",
    "password": "123",
    "name": "Marco Silva"
}
```

#### Response

Responds with the status code and the new Vital Vue User ID.

### Register Assistant

#### Body Example

```json
{
    "username": "assistant name",
    "email": "assistant@mail.com",
    "password": "123",
    "contract_details": "the best assistant",
    "name": "Alexandra"
}
```

#### Response

Responds with the status code and the new Vital Vue User ID.

### Register Nurse

#### Body Example

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

#### Response

Responds with the status code and the new Vital Vue User ID.

### Register Doctor

#### Body Example

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

#### Response

Responds with the status code and the new Vital Vue User ID.

### User Authentication

#### Body Example

```json
{
    "username": "msilva2",
    "password": "123"
}
```

#### Response

Responds with the status code and the authorization token. This token will be automatically used in the remaining requests.

### Schedule Appointment

#### Body Example

```json
{
    "doctor_id": 4,
    "date": "2024-10-23",
    "start_time": "17:30",
    "end_time": "18:00",
    "cost": 100
}
```

#### Response

Responds with the status code and the ID of the new appointment. 

### See Appointments

Responds with the status code and the information about the appointments.

#### Response Example

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

### Schedule Surgery

#### Body Example

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

### Get Prescriptions

Responds with the status code and the information about the patient prescriptions.

#### Response Example

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

### Add Prescription

#### Body Example

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

#### Response

Responds with the status code and the prescription ID.