# VitalVue

---
title: Relatório Base de dados
author:
  - Luís Pedro de Sousa Oliveira Góis, nº 2018280716
  - Marco Manuel Almeida e Silva, nº 2021211653
  - João Vítor Fraga Maia Alves, nº 2016122878
date: date
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

## Attachments

The onda project saved as json are saved under the assets directory, among all
the figures as well.
