import os
from psycopg2.pool import SimpleConnectionPool

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

# create users table for auth
def init_db():
    db_execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR (50) UNIQUE NOT NULL,
                    occupation VARCHAR (50),
                    email VARCHAR (100) UNIQUE NOT NULL,
                    password_hash VARCHAR(100),
                    created_at TIMESTAMP NOT NULL
                );          
    """)

# run database queries (READ OPERATIONS ONLY)
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

# run database write operations
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










