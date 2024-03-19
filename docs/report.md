# VitalVue

---
title: BD Report
author:
  - Luís Pedro de Sousa Oliveira Góis, nº 2018280716
  - Marco Manuel Almeida e Silva, nº 2021211653
  - João Vítor Fraga Maia Alves, nº 2016122878
date: 11/03/2024
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

## Functional Description

This project aims to develop a Hospital Management System (HMS). The development
of the database should fit the required functionalities and business
restrictions to ensure effective storage and information processing and
retrieval.

An HMS is designed to streamline and optimize the operations and workflows
within a healthcare facility. At its core, an HMS serves as a centralized
platform for managing various aspects of hospital administration, including
patient care, scheduling, billing, and resource allocation.

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

## Definition

### Transaction

### Potential concurrency conflicts

## ER Diagram

```mermaid
---
title: Hospital Management System
---
erDiagram
     Appointment {
         BigInt id PK
     }
     Appointment }o--o| Assistant : ""
     Appointment }o--o{ Nurse : ""
     Appointment o|--o{ Prescription : ""
     Bill {
        BigInt id PK
        float cost
     }
     Bill o|--o| Appointment : ""
     Bill o|--o| Hospitalization : ""
     Doctor {
        Int medicalLicense
     }
     Doctor ||--|{ Appointment : ""
     Doctor }|--|{ Field : ""
     Hospitalization {
        BigInt id PK
     }
     Hospitalization ||--|| Nurse : responsible
     Hospitalization o|--o{ Prescription : ""
     Hospitalization o|--|{ Surgery : ""
     Medicine {
        BigInt id PK
        float dosage
     }
     Medicine }|--|{ SideEffect : ""
     Nurse {
        VarChar internalHierachicalCategory
     }
     Nurse }o--o{ Surgery : ""
     Patient {
        BigInt id PK
     }
     Patient ||--o{ Appointment : ""
     Patient ||--o{ Hospitalization : ""
     Payment {
        BigInt id PK
        TimeStamp date
        BigInt payingAmount
     }
     Payment }|--|| Bill : ""
     Prescription {
        BigInt id PK
     }
     Prescription o|--o{ Medicine : ""
     Surgery {
         BigInt id PK
     }
     Surgery }|--|| Doctor : ""

     Employee {
        BigInt id PK
        Text contractDetails
     }
     Nurse }o--|| Employee : is
     Assistant }o--|| Employee : is
     Doctor }o--|| Employee : is
```

## Relational data model

## Development plan
