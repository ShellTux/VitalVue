# VitalVue

---
title: BD Report
author:
  - Luís Pedro de Sousa Oliveira Góis, nº 2018280716
  - Marco Manuel Almeida e Silva, nº 2021211653
  - João Vítor Fraga Maia Alves, nº 2016122878
date: 11/03/2024
---

## Description

This project involves developing a Hospital Management System (HMS) that will
streamline hospital operations by managing patient care, scheduling, billing,
and resource allocation. The system will include functionalities for patients,
doctors, nurses, and assistants, with each having specific attributes and roles.
It will manage appointments, hospitalizations, surgeries, prescriptions, side
effects, and billing, with concurrency issues and triggers considered. Doctors
will have specializations organized hierarchically. any necessary database
schema details that are not explicitly defined should be determined.

## Definition

### Transaction

### Potential concurrency conflicts

## ER Diagram

The primary actors of the system include patients and employees, with the latter
comprising doctors, nurses, and assistants, each with specific attributes (e.g.,
a doctor has information related to his/hers medical license; a nurse has an
internal hierarchical category). All employees have an employee id and the
contract details are also to be stored in the database. The system must be able
to manage the patients’ appointments and hospitalizations for surgeries (each
hospitalization might be associated with multiple surgeries). Each appointment
and surgery is conducted by a doctor and can have multiple nurses involved in
different specific roles. For each hospitalization there is one nurse that is
assigned as responsible. Obviously, no patient, doctor, or nurse can be in two
events at the same time. On the other hand, assistants contribute to the
operational efficiency by scheduling appointments and hospitalizations. Remember
that multiple users (e.g., patients) can use the system simultaneously and thus
concurrency issues must be taken into account. 
 
Each appointment and hospitalization can be associated with prescriptions, which
define the dosage for each medication (each prescription can comprise multiple
medicines). The system also logs a catalog of side effects, and each medicine
has multiple side effects with specific occurrences and severity (multiple
medicines can have the same side effects, with different
probabilities/severity). 
 
The billing for each appointment and hospitalization must also be stored. For
simplicity, let’s assume that each appointment and each surgery has a fixed
cost. Whenever an appointment is scheduled or a surgery is added to a
hospitalization, a bill is created or updated (in the case that a bill had
already been created for previous surgery in a given hospitalization). This
process must be implemented using triggers. Each bill can be split into multiple
payments. 
 
Doctors specialize in various medical fields. Specializations can be
hierarchically organized (i.e., one specialization may have a parent
specialization), allowing for detailed categorization of medical expertise.  
 
Any details that are not specifically defined but that you feel are necessary to
develop the database schema should be explicitly defined.

Entities:

- Patient
- Employee
- Doctor
- Nurse
- Assistant
- Hospitalization
- Surgery
- Appointment
- Prescription
- Medicine
- Side Effect
- Specialization
- Billing
- Payment

Relationships:

- Employee (1) <----> (0,1) Doctor
- Employee (1) <----> (0,1) Nurse
- Employee (1) <----> (0,1) Assistant
- Employee (1) <----> (0,n) Hospitalization
- Doctor (1) <----> (0,n) Surgery
- Doctor (1) <----> (0,n) Appointment
- Nurse (1) <----> (0,n) Surgery
- Nurse (1) <----> (0,n) Appointment
- Appointment (1) <----> (0,n) Prescription
- Prescription (1) <----> (0,n) Medicine
- Medicine (1) <----> (0,n) Side Effect
- Specialization (1) <----> (0,n) Specialization
- Billing (1) <----> (0,n) Payment
- Appointment (1) <----> (0,n) Billing
- Surgery (1) <----> (0,n) Billing

- The primary actors of the system include patients and employees, with the
  latter comprising doctors, nurses, and assistants, each with specific
  attributes. This justifies the relationship between Employee and Doctor,
  Nurse, and Assistant entities.
- All employees have an employee id and the contract details are also to be
  stored in the database. This justifies the relationship between Employee and
  Hospitalization (as employees can be assigned to hospitalizations).
- The system must be able to manage the patients' appointments and
  hospitalizations for surgeries. This justifies the relationships between
  Doctor and Surgery, Appointment entities, as well as Nurse and Surgery,
  Appointment entities.
- For each hospitalization, there is one nurse that is assigned as responsible.
  This justifies the relationship between Nurse and Hospitalization entity.
- Assistants contribute to the operational efficiency by scheduling appointments
  and hospitalizations. This justifies the relationship between Assistant and
  Appointment, Hospitalization entities.
- Multiple users (e.g., patients) can use the system simultaneously and thus
  concurrency issues must be taken into account. This justifies the
  relationships between Patient and Appointment, Hospitalization entities.
- Each appointment and hospitalization can be associated with prescriptions,
  which define the dosage for each medication. This justifies the relationship
  between Appointment and Prescription entities.
- The system logs a catalog of side effects, and each medicine has multiple side
  effects with specific occurrences and severity. This justifies the
  relationship between Medicine and Side Effect entities.
- Each billing can be split into multiple payments. This justifies the
  relationship between Billing and Payment entities.
- Doctors specialize in various medical fields. This justifies the relationship
  between Doctor and Specialization entity.


## Relational data model

## Development plan
