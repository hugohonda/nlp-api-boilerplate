from app.utils.logging import logger
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

USERS_TABLE = "users"


class PostgresClient:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            logger.info("Connected to PostgreSQL")
        except (Exception, psycopg2.Error) as error:
            logger.error(f"Error while connecting to PostgreSQL: {error}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            logger.info("Disconnected from PostgreSQL.")

    def create_users_table(self):
        try:
            columns = """
                username TEXT PRIMARY KEY,
                fullname TEXT,
                email TEXT,
                hashed_password TEXT,
                disabled BOOLEAN
            """
            cursor = self.connection.cursor()
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {USERS_TABLE} ({columns});")
            self.connection.commit()
            logger.info("Table created successfully")
        except (Exception, psycopg2.Error) as error:
            logger.error(f"Error creating table: {error}")

    def insert_user(self, table_name, user_data):
        try:
            columns = ", ".join(user_data.keys())
            values = tuple(user_data.values())
            query = f"""
                INSERT INTO {table_name} ({columns})
                VALUES {values}
                ON CONFLICT (username)
                DO NOTHING;
            """
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            logger.info("User inserted successfully")
        except (Exception, psycopg2.Error) as error:
            logger.error(f"Error inserting user: {error}")

    def seed_users_data(self, data):
        try:
            for record in data:
                self.insert_user(USERS_TABLE, record)
            logger.info("Data seeded successfully")
        except (Exception, psycopg2.Error) as error:
            logger.error(f"Error seeding data: {error}")

    def check_user_exists(self, username):
        try:
            query = f"SELECT * FROM {USERS_TABLE} WHERE username = '{username}' LIMIT 1;"
            cursor = self.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            if len(rows) > 0:
                columns = [desc[0] for desc in cursor.description]
                user_data = dict(zip(columns, rows[0]))
                logger.info("User retrieved successfully")
                return user_data
            else:
                return None
        except (Exception, psycopg2.Error) as error:
            logger.error(f"Error checking user existence: {error}")
            return False


client = PostgresClient(
    host=os.getenv('POSTGRES_HOST', 'postgres'),
    port=os.getenv('POSTGRES_PORT', '5432'),
    database=os.getenv('POSTGRES_DB', 'apidb'),
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', 'changeme'),
)

client.connect()
client.create_users_table()

fake_users_db = [
    {
        "username": "teste",
        "fullname": "Teste Teste",
        "email": "teste@teste.com",
        "hashed_password": "$2b$12$dcU.TRVClCu.390jYXDTdeJb/KjNYB/PcOj/ihmDyOj2G/GWeUHlW",
        "disabled": False
    }
]

client.seed_users_data(fake_users_db)
