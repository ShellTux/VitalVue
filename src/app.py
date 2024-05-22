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
import psycopg2

CONFIG = dotenv_values('.env')

# setup flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key' #TODO Create config setting for secret key

# setup Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'secret_key' #TODO Create config setting for jwt secret key
jwt = JWTManager(app)

# declare logger
logger = logging.getLogger('logger')

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

################################################################################
## LANDING PAGE
################################################################################

@app.route('/')
def landing_page():
    return """<!DOCTYPE html>
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
    logger.info(f'POST {request.path}')

    payload = request.get_json()

    #if registration_type not in IndividualTypes:
    #    return jsonify({'status': StatusCode.API_ERROR.value,
    #                    'error': 'Invalid registration type'})

    individual = IndividualTypes(registration_type)
    values = individual.get_values()
    response = validate_payload(payload, values)

    if response:
        return jsonify(response)

    statement = individual.sql_insert_statement()
    input_values = [payload[key] for key in values]

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(statement, input_values)

        # TODO Update this endpoint so that it returns the user id if successful

        conn.commit()
        response = {'status': StatusCode.SUCCESS.value,
                    'results': 'Registered new individual'}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST {request.path} - error: {error}')
        response = {'status': StatusCode.INTERNAL_ERROR.value,
                    'error': str(error)}
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()

    return jsonify(response)

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

    payload = request.get_json()

    statement = """
                SELECT u.username, u.password, u.type
                FROM vital_vue_user AS u
                WHERE u.username = %s AND u.password = %s;
                """
    values = ['username', 'password']
    input_values = [payload[key] for key in values]

    response = validate_payload(payload, values)
    if response:
        return jsonify(response)

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(statement, input_values)
        rows = cursor.fetchall()

        if rows:
            row = rows[0]
            access_token = create_access_token(identity=payload['username'])
            response = {'status': StatusCode.SUCCESS.value,
                        'results': access_token}
        else:
            response = {'status': StatusCode.API_ERROR.value, 
                        'results': 'Invalid login credentials'}
            
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
## SEE APPOINTMENTS
## -- only assistants and target patients
## 
################################################################################

@app.route('/appointments/<patient_user_id>/', methods=['GET'])
@jwt_required()
def see_appointments(patient_user_id):
    logger.info(f'GET {request.path}')

    token = get_jwt()
    identity = get_jwt_identity()
    payload = request.get_json()

    statement = """
                    SELECT *
                    FROM appointment AS ap
                    WHERE ap.patient_id = %s
                """
    statement_values = (patient_user_id,)

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(statement, statement_values)
        rows = cursor.fetchall()

        response = {'status': StatusCode.SUCCESS.value}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET {request.path} - error: {error}')
        response = {'status': StatusCode.INTERNAL_ERROR.value, 
                    'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    response = {'status': StatusCode.SUCCESS.value}

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
## GET PRESCRIPTIONS
## -- only employees and target patient
## 
################################################################################

@app.route('/prescriptions/<person_id>/', methods = ['GET'])
@jwt_required()
def get_prescriptions(person_id):
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
        rows = cursor.fetchall()

        results = []
        for row in rows:
            results.append({})

        response = {'status': StatusCode.SUCCESS.value, 
                    'results': results}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET {request.path} - error: {error}')
        response = {'status': StatusCode.INTERNAL_ERROR.value, 
                    'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    response = {'status': StatusCode.SUCCESS.value}

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

################################################################################
## DAILY SUMMARY
## -- only assistants
## 
################################################################################

@app.route('/daily/<year_month_day>/', methods = ['GET'])
@jwt_required()
def daily_summary(year_month_day):
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

################################################################################
## GENERATE MONTHLY REPORT
## -- only assistants
## 
################################################################################

@app.route('/report/', methods = ['GET'])
@jwt_required()
def generate_monthly_report():
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
