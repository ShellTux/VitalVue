################################################################################
# Project                          ___ ___ __ __         __ ___ ___             
#                                 |   Y   |__|  |_.---.-|  |   Y   .--.--.-----.
#                                 |.  |   |  |   _|  _  |  |.  |   |  |  |  -__|
#                                 |.  |   |__|____|___._|__|.  |   |_____|_____|
#                                 |:  1   |                |:  1   |            
#                                  \:.. ./                  \:.. ./             
#                                   `---'                    `---'              
#
# Authors:
#   João Alves,  2016122878
#   Luís Góis,   2018280716
#   Marco Silva, 2021211653
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#
# You may opt to use, copy, modify, merge, publish, distribute and/or sell
# copies of the Software, and permit persons to whom the Software is
# furnished to do so, under the terms of the LICENSE file.
#
# This software is distributed on an "AS IS" basis, WITHOUT WARRANTY OF ANY
# KIND, either express or implied.
#
################################################################################

from dotenv import dotenv_values

from flask import Flask
from flask import request
from flask import jsonify

from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt

from StatusCode import StatusCode
from IndividualTypes import IndividualTypes

import logging
from logging.config import fileConfig
import psycopg2
import hashlib

CONFIG = dotenv_values('.env')

# setup flask app
app = Flask(__name__)
# TODO: Create config setting for secret key
app.config['SECRET_KEY'] = 'secret_key'

# setup Flask-JWT-Extended extension
# TODO: Create config setting for jwt secret key
app.config['JWT_SECRET_KEY'] = 'secret_key'
jwt = JWTManager(app)

fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def connect_db(
        *,
        user: str | None     = CONFIG.get('POSTGRES_USER'),
        password: str | None = CONFIG.get('POSTGRES_PASSWORD'),
        host: str | None     = CONFIG.get('DB_HOST'),
        port: str | None     = CONFIG.get('DB_PORT'),
        database: str | None = CONFIG.get('POSTGRES_DB')
        ):
    return psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=str(port),
            database=database
            )

def validate_payload(payload, values):
    for value in values:
        if value not in payload:
            return {'status': StatusCode.API_ERROR.value,
                    'results': f'{value} value not in payload'}
    return {}

def hash_password(password):
    password_bytes = password.encode()
    encoded = hashlib.md5(password_bytes)
    return encoded.hexdigest()

################################################################################
## LANDING PAGE
################################################################################

@app.route('/')
def landing_page():
    return r"""<!DOCTYPE html>
<html>
<body>
    <pre style="font-size: 20px;">
 ___ ___ __ __         __ ___ ___
|   Y   |__|  |_.---.-|  |   Y   .--.--.-----.
|.  |   |  |   _|  _  |  |.  |   |  |  |  -__|
|.  |   |__|____|___._|__|.  |   |_____|_____|
|:  1   |                |:  1   |
 \:.. ./                  \:.. ./
  `---'                    `---'
    </pre>
</body>
</html>"""

################################################################################
## REGISTER NEW INDIVIDUAL
##
## Registers a new individual taking the type into consideration
##
## How to use in curl:
## > curl -X POST http://localhost:5433/register/patient - H 'Content-Type: application/json' - d ''
################################################################################

@app.route('/register/<registration_type>/', methods=['POST'])
def register(registration_type: str):
    endpoint = f'{request.method} {request.path}'
    logger.info(endpoint)

    # 1. get request payload
    payload = request.get_json()

    # 2. validate registration type
    if registration_type not in IndividualTypes:
       return jsonify({'status': StatusCode.API_ERROR.value,
                       'error': 'Invalid registration type'})

    # 3. get individual statement and key values
    individual = IndividualTypes(registration_type)
    logging.debug(individual.value)
    statement = individual.sql_insert_statement()
    key_values = individual.get_values()

    # 4. validate payload
    response = validate_payload(payload, key_values)
    if response:
        return jsonify(input_values)

    # 5. get input values from payload
    payload['password'] = hash_password(payload['password'])
    input_values = [payload[key] for key in key_values]

    # 6. connect to database
    connection = connect_db()
    cursor = connection.cursor()

    logger.debug(statement)

    try:
        cursor.execute(statement, input_values)
        user_id = cursor.fetchone()[0]
        input_values = {'status': StatusCode.SUCCESS.value,
                        'results': user_id}
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'{endpoint} - error: {error}')
        input_values = {'status': StatusCode.INTERNAL_ERROR.value,
                        'error': str(error)}
        connection.rollback()

    finally:
        if connection is not None:
            connection.close()

    return jsonify(input_values)

################################################################################
## USER AUTHENTICATION
##
## Login using the username and password. In case of success, the returning
## token will be included in the header of the remaining requests.
##
## How to use in curl:
## > curl -X PUT http://localhost:8080/user -H 'Content-Type: application/json -d
##   {"username": username, "password": password}
################################################################################

@app.route('/user/', methods=['PUT'])
def user_authentication():
    logger.info(f'PUT {request.path}')

    # 1. get request payload
    payload = request.get_json()

    # 2. query statement and key values
    statement = """
                SELECT 
                    u.id, 
                    u.type
                FROM 
                    vital_vue_user AS u
                WHERE 
                    u.username = %s 
                    AND u.password = %s;
                """
    key_values = ['username', 'password']

    # 3. validate payload
    response = validate_payload(payload, key_values)
    if response:
        return jsonify(response)

    # 5. get input values from payload
    payload['password'] = hash_password(payload['password'])
    input_values = [payload[key] for key in key_values]

    # 6. connect to database
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(statement, input_values)
        rows = cursor.fetchall()

        if rows:
            row = rows[0]
            access_token = create_access_token(identity = row[0],
                                               additional_claims = {
                                                   'type': row[1]
                                                   })
            response = {'status': StatusCode.SUCCESS.value,
                        'results': access_token}
        else:
            response = {'status': StatusCode.API_ERROR.value, 
                        'results': 'Invalid authentication credentials'}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'PUT {request.path} - error: {error}')
        response = {'status': StatusCode.INTERNAL_ERROR.value,
                    'error': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return jsonify(response)

################################################################################
## SCHEDULE APPOINTMENT
## -- only patients
## 
################################################################################

@app.route('/appointment/', methods=['POST'])
@jwt_required()
def schedule_appointment():
    logger.info(f'POST {request.path}')

    # 1. get token data
    id = get_jwt_identity()
    type = get_jwt().get('type')

    # 2. validate caller
    if type != IndividualTypes.PATIENT:
        response = {'status': StatusCode.API_ERROR, 
                    'errors': 'Only patients can use this endpoint'}
        return jsonify(response)
    
    # 3. get request payload
    payload = request.get_json()

    # 4. query statement and key values
    statement = """
                INSERT INTO 
                    appointment (
                        doctor_employee_vital_vue_user_id,
                        scheduled_date,
                        start_time,
                        end_time,
                        cost,
                        patient_vital_vue_user_id
                    )
                VALUES (
                    %s, %s, %s, %s, %s, %s
                )
                RETURNING 
                    id;
                """
    key_values = ['doctor_id', 'date', 
                  'start_time', 'end_time', 
                  'cost']

    # 5. validate payload
    response = validate_payload(payload, key_values)
    if response:
        return jsonify(response)
    
    # 6. get input values
    payload['start_time'] = payload['date'] + ' ' + payload['start_time']
    payload['end_time'] = payload['date'] + ' ' + payload['end_time']
    input_values = [payload[key] for key in key_values]
    input_values.append(id)

    # 7. connect to database
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(statement, input_values)
        appointment_id = cursor.fetchone()[0]
        response = {'status': StatusCode.SUCCESS.value, 
                    'results': appointment_id}
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST {request.path} - error: {error}')
        response = {'status': StatusCode.INTERNAL_ERROR.value, 
                    'errors': str(error)}
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()

    return jsonify(response)

################################################################################
## SEE APPOINTMENTS
## -- only assistants and target patients
## 
################################################################################

@app.route('/appointments/<patient_user_id>/', methods=['GET'])
@jwt_required()
def see_appointments(patient_user_id):
    logger.info(f'GET {request.path}')

    # 1. get token data
    id = get_jwt_identity()
    type = get_jwt().get('type')

    # 2. check if endpoint is accessible to caller
    allowed = [IndividualTypes.ASSISTANT, IndividualTypes.PATIENT]
    if type not in allowed:
        response = {'status': StatusCode.API_ERROR.value, 
                    'errors': "You don't have permission to see patient appointments"}
        return jsonify(response)
    if type == IndividualTypes.PATIENT and id != patient_user_id:
        response = {'status': StatusCode.API_ERROR.value, 
                    'errors': 'You are not the target patient'}
        return jsonify(response)
            
    # 3. query statement and key values
    statement = """
                SELECT 
                    ap.id,
                    ap.doctor_employee_vital_vue_user_id,
                    ap.scheduled_date
                FROM 
                    appointment AS ap
                WHERE 
                    ap.patient_vital_vue_user_id = %s
                """
    statement_values = (patient_user_id,)

    # 4. connect to database
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(statement, statement_values)
        rows = cursor.fetchall()

        if rows:
            results = []
            for row in rows:
                content = {'id': row[0], 'doctor_id': row[1], 'date': row[2]}
                results.append(content)
        else:
            results = 'No available appointments'

        response = {'status': StatusCode.SUCCESS.value, 
                    'results': results}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET {request.path} - error: {error}')
        response = {'status': StatusCode.INTERNAL_ERROR.value, 
                    'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return jsonify(response)

################################################################################
## SCHEDULE SURGERY
## -- only assistants
## 
################################################################################

@app.route('/surgery/', defaults = {'hospitalization_id': None}, methods = ['POST'])
@app.route('/surgery/<hospitalization_id>/', methods = ['POST'])
@jwt_required()
def schedule_surgery(hospitalization_id):
    logger.info(f'{request.method} {request.path}')

    # 1. get token data
    id = get_jwt_identity()
    type = get_jwt().get('type')

    # 2. validate caller
    if type != IndividualTypes.ASSISTANT:
        response = {'status': StatusCode.API_ERROR.value, 
                    'errors': 'Only assistants can use this endpoint'}
        return jsonify(response)
    
    # 3. get request payload
    payload = request.get_json()

    # 4. query statement and key values
    statement = """
                WITH new_surgery AS (
                    INSERT INTO surgery (
                        patient_vital_vue_user_id,
                        doctor_employee_vital_vue_user_id,
                        scheduled_date,
                        start_time,
                        end_time,
                        hospitalization_id
                    )
                    VALUES (
                        %s, %s, %s, %s, %s<, %s>
                    )
                    RETURNING
                        id
                )
                INSERT INTO nurse_role (
                    surgery_id,
                    nurse_employee_vital_vue_user_id,
                    role
                )
                SELECT
                    ns.id,
                    nurse_employee_vital_vue_user_id,
                    role
                FROM 
                    new_surgery ns,
                    (VALUES (%s, %s)) AS nurse_role(nurse_employee_vital_vue_user_id, role);
                SELECT 
                    hospitalization_id,
                    id,
                    patient_vital_vue_user_id,
                    doctor_employee_vital_vue_user_id,
                    scheduled_date
                FROM
                    new_surgery;
                """
    key_values = ['patient_user_id', 'doctor_user_id', 'nurses', 
                  'date', 'start_time', 'end_time']
    if hospitalization_id is None:
        # remove 'hospitalization_id' column from statement
        column_substr = 'hospitalization_id'
        index = statement.find(column_substr)
        statement = statement[:index] + statement[index + len(column_substr):]
        statement.replace('end_time,', 'end_time')

    # 5. validate payload
    response = validate_payload(payload, key_values)
    if response:
        return jsonify(response)
    
    # 6. get input values
    payload['start_time'] = payload['date'] + ' ' + payload['start_time']
    payload['end_time'] = payload['date'] + ' ' + payload['end_time']
    nurses = payload['nurses']
    key_values.remove('nurses')
    input_values = [payload[key] for key in key_values]
    if hospitalization_id is not None:
        input_values.append(hospitalization_id)
        statement.replace('<, %s>', ', %s')
    else:
        statement.replace('<, %s>', '')
    input_nurses = [item for nurse in nurses for item in nurse]
    input_values.extend(input_nurses)

    logging.debug(statement)
    logging.debug(input_values)

    # 7. connect to database
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(statement, input_values)
        row = cursor.fetchone()[0]
        results = {'hospitalization_id': row[0],
                   'surgery_id': row[1],
                   'patient_id': row[2],
                   'doctor_id': row[3],
                   'date': row[4]}
        response = {'status': StatusCode.SUCCESS.value, 
                    'results': results}
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST {request.path} - error: {error}')
        response = {'status': StatusCode.INTERNAL_ERROR.value, 
                    'errors': str(error)}
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()

    return jsonify(response)

################################################################################
## GET PRESCRIPTIONS
## -- only employees and target patient
## 
################################################################################

@app.route('/prescriptions/<person_id>/', methods = ['GET'])
@jwt_required()
def get_prescriptions(person_id):
    logger.info(f'GET {request.path}')

    # 1. get token data
    id = get_jwt_identity()
    type = get_jwt().get('type')

    # 2. check if patient is target patient
    if type == IndividualTypes.PATIENT and id != person_id:
        return jsonify({'status': StatusCode.API_ERROR.value, 
                        'errors': 'Only the target patient can use this endpoint'})

    # 3. query statement and values
    statement = """
                SELECT 
                    p.prescription_id, 
                    p.validity_date
                FROM 
                    prescription AS p
                WHERE 
                    p.patient_vital_vue_user_id = %s
                """
    values = (person_id,)
    
    # 4. connect to database
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(statement, values)
        rows = cursor.fetchall()

        if rows:
            results = []
            for row in rows:
                content = {'prescription_id': row[0], 
                           'validity_date': row[1]}
                results.append(content)
        else:
            results = 'This patient has no prescriptions'
        
        response = {'status': StatusCode.SUCCESS.value, 
                    'results': results}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET {request.path} - error: {error}')
        response = {'status': StatusCode.INTERNAL_ERROR.value, 
                    'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return jsonify(response)

################################################################################
## ADD PRESCRIPTIONS
## -- only doctors
## 
################################################################################

@app.route('/prescription/', methods = ['POST'])
@jwt_required()
def add_prescription():
    logger.info(f'POST {request.path}')

    token = get_jwt()
    identity = get_jwt_identity()
    payload = request.get_json()

    conn = connect_db()
    cursor = conn.cursor()

    statement = ""
    values = ""

    try:
        cursor.execute(statement, values)

        results = []
        response = {'status': StatusCode.SUCCESS.value, 
                    'results': results}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST {request.path} - error: {error}')
        response = {'status': StatusCode.INTERNAL_ERROR.value, 
                    'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return jsonify(response)

################################################################################
## EXECUTE PAYMENT
## -- only the owning patient
## 
################################################################################

@app.route('/bills/<bill_id>', methods = ['POST'])
@jwt_required()
def execute_payment(bill_id):
    logger.info(f'POST {request.path}')

    token = get_jwt()
    identity = get_jwt_identity()
    payload = request.get_json()

    conn = connect_db()
    cursor = conn.cursor()

    statement = ""
    values = ""

    try:
        cursor.execute(statement, values)

        results = []
        response = {'status': StatusCode.SUCCESS.value, 
                    'results': results}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST {request.path} - error: {error}')
        response = {'status': StatusCode.INTERNAL_ERROR.value, 
                    'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return jsonify(response)

################################################################################
## LIST TOP 3 PATIENTS
## -- only assistants
## 
################################################################################

@app.route('/top3/', methods = ['GET'])
@jwt_required()
def list_top3_patients():
    logger.info(f'GET {request.path}')

    token = get_jwt()
    identity = get_jwt_identity()
    payload = request.get_json()

    conn = connect_db()
    cursor = conn.cursor()

    statement = ""
    values = ""

    try:
        cursor.execute(statement, values)

        results = []
        response = {'status': StatusCode.SUCCESS.value, 
                    'results': results}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET {request.path} - error: {error}')
        response = {'status': StatusCode.INTERNAL_ERROR.value, 
                    'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return jsonify(response)

@app.route('/daily/<year_month_day>/', methods = ['GET'])
@jwt_required()
def daily_summary(year_month_day: str):
    r'''
    Daily Summary.

    List a count for all hospitalizations details of a given day. Consider,
    surgeries, payments, and prescriptions. Just one SQL query should be used to
    obtain the information. Only assistants can use this endpoint.
    '''
    endpoint = f'{request.method} {request.path}'
    logger.info(endpoint)

    token = get_jwt()
    identity = get_jwt_identity()
    individual_type = token.get('type')

    if individual_type != IndividualTypes.ASSISTANT:
        response = {'status': StatusCode.API_ERROR.value, 
                    'errors': "You don't have permission to see daily summary"}
        return jsonify(response)

    # TODO: This sql statement gives all results grouped by date, not by the
    # given day.
    statement = '''
        SELECT
            SUM(payment.amount) AS "Amount Spent",
            COUNT(surgery.id) AS "Surgeries",
            COUNT(prescription.id) AS Prescriptions
        FROM
            hospitalization
        LEFT JOIN
            hospitalization_bill ON hospitalization.id = hospitalization_bill.hospitalization_id
        LEFT JOIN
            bill ON hospitalization_bill.bill_id = bill.id
        LEFT JOIN
            payment ON bill.id = payment.bill_id
        LEFT JOIN
            surgery ON hospitalization.id = surgery.hospitalization_id
        LEFT JOIN
            prescription ON hospitalization.id = prescription.hospitalization_id
        WHERE
            hospitalization.assistant_employee_vital_vue_user_id IN (SELECT employee_vital_vue_user_id FROM assistant)
        GROUP BY
            date(scheduled_date);
    '''
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(statement)
        rows = cursor.fetchall()

        if len(rows) == 0:
            results = list(map(lambda row: {
                'amount_spent': row[0],
                'surgeries': row[1],
                'prescriptions': row[2]
                }, rows))
        else:
            results = 'No available hospitalizations'

        response = {
                'status': StatusCode.SUCCESS.value,
                'results': results
                }

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET {request.path} - error: {error}')
        response = {'status': StatusCode.INTERNAL_ERROR.value, 
                    'errors': str(error)}

    finally:
        if connection is not None:
            connection.close()

    return jsonify(response)

@app.route('/report/', methods = ['GET'])
@jwt_required()
def generate_monthly_report():
    r'''
    Generate monthly report

    Get a list of the doctors with more surgeries each month in the last 12
    months. Just one SQL query should be used to obtain the information. Only
    assistants can use this endpoint.
    '''
    endpoint = f'{request.method} {request.path}'
    logger.info(endpoint)

    token = get_jwt()
    individualType = token.get('type')

    if individualType != IndividualTypes.ASSISTANT:
        response = {'status': StatusCode.API_ERROR.value, 
                    'errors': 'Only assistants can use this endpoint'}
        return jsonify(response)

    statement = '''
        SELECT
            EXTRACT(MONTH FROM s.scheduled_date) AS Mês,
            e.name as "Nome do Doctor",
            COUNT(s.scheduled_date) as "Total de cirurgias"
        FROM
            employee e
        JOIN
            doctor d ON e.vital_vue_user_id = d.employee_vital_vue_user_id
        JOIN
            surgery s ON d.employee_vital_vue_user_id = s.doctor_employee_vital_vue_user_id
        WHERE
            s.scheduled_date >= DATE_TRUNC('month', NOW() - INTERVAL '12 months')
        GROUP BY
            e.name, EXTRACT(MONTH FROM s.scheduled_date)
        ORDER BY
            "Total de cirurgias" DESC;
    '''

    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(statement)
        rows = cursor.fetchall()

        results = []
        if rows:
            for row in rows:
                results.append({
                    'month': row[0],
                    'doctor': row[1],
                    'surgeries': row[2]
                    })

        if len(results) == 0:
            results = 'No available surgeries in the last 12 months'

        response = {
                'status': StatusCode.SUCCESS.value,
                'results': results
                }

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'{endpoint} - error: {error}')
        response = {'status': StatusCode.INTERNAL_ERROR.value, 
                    'errors': str(error)}

    finally:
        if connection is not None:
            connection.close()

    return jsonify(response)

################################################################################
## ENTRY POINT
################################################################################

def main():
    # set up logging
    logging.basicConfig(filename='vitalvue.log')
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]:  %(message)s', '%H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # run application
    port = 8080 if CONFIG['SERVER_PORT'] is None else int(CONFIG['SERVER_PORT'])
    url = f'http://{CONFIG.get("SERVER_HOST")}:{port}/'
    logger.info(f"Vital Vue API v1.0 online: {url}")
    app.run(
            host=CONFIG.get('SERVER_HOST'),
            debug=True,
            threaded=True,
            port=port
            )

if __name__ == "__main__":
    main()
