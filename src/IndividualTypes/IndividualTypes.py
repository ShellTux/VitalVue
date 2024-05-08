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
        return {
                cls.ASSISTANT: ['id', 'contract_details'],
                cls.DOCTOR:    ['id', 'contract_details'],
                cls.DOCTOR:    ['id', 'contract_details'],
                cls.PATIENT:   ['id']
                }

    def get_values(self) -> list[str]:
        return IndividualTypes.values_handlers()[self]

    @classmethod
    def sql_insert_statement_handlers(cls):
        return {
            cls.DOCTOR:    r"""
            INSERT INTO employee (id, contract_details)
            VALUES (%d, %s);
            """,
            cls.NURSE:     r"""
            INSERT INTO employee (id, contract_details)
            VALUES (%d, %s);
            """,
            cls.ASSISTANT: r"""
            INSERT INTO employee (id, contract_details)
            VALUES (%d, %s);
            """,
            cls.PATIENT:   r"""
            INSERT INTO patient (id)
            VALUES (%s);
            """
            }

    def sql_insert_statement(self):
        return IndividualTypes.sql_insert_statement_handlers()[self]
