from load_env import ENV
import psycopg2

def connect_db(
        *,
        user: str,
        password: str,
        host: str,
        port: str,
        database: str):
    return psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=str(port),
            database=database
            )

if __name__ == "__main__":
    connection = connect_db(
            user=ENV['USER'],
            password=ENV['PASSWORD'],
            host=ENV['HOST'],
            port=ENV['PORT'],
            database=ENV['DATABASE']
            )
    cursor = connection.cursor()
