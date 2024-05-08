################################################################################
# Project                          ___ ___ __ __         __ ___ ___             
#                                 |   Y   |__|  |_.---.-|  |   Y   .--.--.-----.
#                                 |.  |   |  |   _|  _  |  |.  |   |  |  |  -__|
#                                 |.  |   |__|____|___._|__|.  |   |_____|_____|
#                                 |:  1   |                |:  1   |            
#                                  \:.. ./                  \:.. ./             
#                                   `---'                    `---'              
#
# Author: João Alves,  2016122878
# Author: Luís Góis,   2018280716
# Author: Marco Silva, 2021211653
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
from flask import Flask, request, jsonify
from StatusCode import StatusCode
from IndividualTypes import IndividualTypes
import logging
import psycopg2

CONFIG = dotenv_values('.env')
app = Flask(__name__)

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
## Registers a new individual taking the individual type into consideration
##
## How to use in curl:
## > curl -X POST http://localhost:5433/register/patient - H 'Content-Type: application/json' - d ''
################################################################################

@app.route('/register/<registration_type>', methods=['POST'])
def register(registration_type: str):
    #logger.info('POST /register/<registration_type>')
    payload = request.get_json()

    if registration_type not in IndividualTypes:
        return jsonify({'status': StatusCode.API_ERROR.value,
                        'error': 'Invalid registration type'})

    individual = IndividualTypes(registration_type)
    print(individual.value)

    conn = connect_db()
    cursor = conn.cursor()

    #TODO: Complete statement and values based on registration type
    #TODO: Validate arguments values
    values = individual.get_values()
    response = validate_payload(payload, values)

    if response:
        jsonify(response)

    statement_values = [payload[key] for key in values]

    try:
        cursor.execute(individual.sql_insert_statement(), statement_values)

        conn.commit()
        response = { 'status': StatusCode.SUCCESS.value,
                    'results': 'Registered new individual' }

    except (Exception, psycopg2.DatabaseError) as error:
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
    payload = request.get_json()

    response = {'status': StatusCode.SUCCESS.value}

    return jsonify(response)

################################################################################
## SCHEDULE APPOINTMENT
##
## 
################################################################################

@app.route('/appointment/', methods=['POST'])
def schedule_appointment():
    payload = request.get_json()

    conn = connect_db()
    cursor = conn.cursor()

    response = {'status': StatusCode.SUCCESS.value}

    return jsonify(response)

################################################################################
## SEE APPOINTMENTS
##
## 
################################################################################

@app.route('/appointments/<patient_user_id>/', methods=['GET'])
def see_appointments(patient_user_id):
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
        response = {'status': StatusCode.INTERNAL_ERROR.value, 'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    response = {'status': StatusCode.SUCCESS.value}

    return jsonify(response)

################################################################################

def main():
    # set up logging
    logging.basicConfig(filename='log_file.log')
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]:  %(message)s', '%H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    port = 8080 if CONFIG['SERVER_PORT'] is None else int(CONFIG['SERVER_PORT'])
    url = f'http://{CONFIG.get("SERVER_HOST")}:{port}/'
    app.run(
            host=CONFIG.get('SERVER_HOST'),
            debug=True,
            threaded=True,
            port=port
            )
    logger.info(f"API v1.0 online: {url}")

if __name__ == "__main__":
    main()
