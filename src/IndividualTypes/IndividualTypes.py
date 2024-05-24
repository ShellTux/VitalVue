from enum import Enum, StrEnum, auto

class IndividualTypes(StrEnum):
    ASSISTANT = auto()
    DOCTOR    = auto()
    NURSE     = auto()
    PATIENT   = auto()

    @classmethod
    def _missing_(cls, value):
        if type(value) != str:
            return None

        value = value.lower()

        for member in cls:
            if member.value == value:
                return member

        print('not found')
        return None

    @classmethod
    def values_handlers(cls):
        base = ['username', 'email', 'password']
        base_employee = base.append(['contract_details', 'username'])
        return {
                cls.DOCTOR:    ['username', 'password', 'email', 
                                'name', 'contract_details',
                                'license'],
                cls.NURSE:     ['username', 'password', 'email', 
                                'name', 'contract_details',
                                'category'],
                cls.ASSISTANT: ['username', 'password', 'email', 
                                'name', 'contract_details'],
                cls.PATIENT:   ['username', 'password', 'email',
                                'name']
                }

    def get_values(self) -> list[str]:
        return IndividualTypes.values_handlers()[self]

    @classmethod
    def sql_insert_statement_handlers(cls):
        return {
            cls.DOCTOR:    """
            WITH new_user AS (
                INSERT INTO vital_vue_user (username, password, email, type)
                VALUES (%s, %s, %s, 'doctor')
                RETURNING id
            ), new_employee AS (
                INSERT INTO employee (name, contract_details, vital_vue_user_id)
                SELECT %s, %s, id FROM new_user
                RETURNING vital_vue_user_id
            )
            INSERT INTO doctor (license, employee_vital_vue_user_id)
            SELECT %s, vital_vue_user_id FROM new_employee
            RETURNING employee_vital_vue_user_id;
            """,
            cls.NURSE:     """
            WITH new_user AS (
                INSERT INTO vital_vue_user (username, password, email, type)
                VALUES (%s, %s, %s, 'nurse')
                RETURNING id
            ), new_employee AS (
                INSERT INTO employee (name, contract_details, vital_vue_user_id)
                SELECT %s, %s, id FROM new_user
                RETURNING vital_vue_user_id
            )
            INSERT INTO nurse (category, employee_vital_vue_user_id)
            SELECT %s, vital_vue_user_id FROM new_employee
            RETURNING employee_vital_vue_user_id;
            """,
            cls.ASSISTANT: """
            WITH new_user AS (
                INSERT INTO vital_vue_user (username, password, email, type)
                VALUES (%s, %s, %s, 'assistant')
                RETURNING id
            ), new_employee AS (
                INSERT INTO employee (name, contract_details, vital_vue_user_id)
                SELECT %s, %s, id FROM new_user
                RETURNING vital_vue_user_id
            )
            INSERT INTO assistant (employee_vital_vue_user_id)
            SELECT vital_vue_user_id FROM new_employee
            RETURNING employee_vital_vue_user_id;
            """,
            cls.PATIENT:   """
            WITH new_user AS (
                INSERT INTO vital_vue_user (username, password, email, type)
                VALUES (%s, %s, %s, 'patient')
                RETURNING id
            )
            INSERT INTO patient (name, vital_vue_user_id)
            SELECT %s, id FROM new_user
            RETURNING vital_vue_user_id;
            """
            }

    def sql_insert_statement(self):
        return IndividualTypes.sql_insert_statement_handlers()[self]
