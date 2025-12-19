import os
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ['POSTGRES_HOST']
DB_USER = os.environ['POSTGRES_USER']
DB_PASSWORD = os.environ['POSTGRES_PASSWORD']
DB_PORT = os.environ['POSTGRES_PORT']
DB_NAME = os.environ['POSTGRES_DB']

# a simple sonnection pool

"""DB connections are expensive!! This Simple pool keeps small set of pre-opened db connections and reuses them. Essentially, each service borrows a connection."""
pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# create resume table
#  Status options: uploaded/parsing/parsed/matched
def init_db():
    db_execute("""
                CREATE TABLE IF NOT EXISTS resumes (
                    id SERIAL PRIMARY KEY,
                    user_id INT REFERENCES users(id),
                    s3_key VARCHAR(500) NOT NULL,
                    status VARCHAR(100) DEFAULT 'uploaded',
                    uploaded_at TIMESTAMP NOT NULL
                );           
    """, (None,))
    print("Resumes table created!")


def db_query(query: str, params: tuple=()):
    """Runs SELECT queries only and returns results"""
    conn = pool.getconn()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        return rows
    # put the connection back into pool
    finally:
        pool.putconn(conn)


def db_execute(query: str, params: tuple=()):
    """Runs INSERT/UPDATE/DELETE queries and commits"""
    conn = pool.getconn()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()
    finally:
        pool.putconn(conn)









