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
from flask import Flask
import logging
import psycopg2

from enum import Enum

class StatusCode(Enum):
    SUCCESS        = 200
    API_ERROR      = 400
    INTERNAL_ERROR = 500

CONFIG = dotenv_values('.env')
app = Flask(__name__)

def connect_db(
        *,
        user: str | None     = CONFIG.get('USER'),
        password: str | None = CONFIG.get('PASSWORD'),
        host: str | None     = CONFIG.get('SERVER_HOST'),
        port: str | None     = CONFIG.get('SERVER_PORT'),
        database: str | None = CONFIG.get('DATABASE')
        ):
    return psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=str(port),
            database=database
            )

@app.route('/')
def landing_page():
    return """
    Hello World (Python Native)!  <br/>
    <br/>
    Check the sources for instructions on how to use the endpoints!<br/>
    <br/>
    BD 2023-2024 Team<br/>
    <br/>
    """

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

    port = 5000 if CONFIG['SERVER_PORT'] is None else int(CONFIG['SERVER_PORT'])
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
