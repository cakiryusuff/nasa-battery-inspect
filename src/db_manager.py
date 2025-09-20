import psycopg2
from src.logger import get_logger

logger = get_logger(__name__)

class DBManager:
    def __init__(self, db_name, db_user, db_password, db_host):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.connection = None
        self.connect()
        
    def connect(self):
        self.connection = psycopg2.connect(
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host
        )
        logger.info("Connected to database")
        self._init_db()
        
    def _init_db(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            voltage_measured FLOAT,
            current_measured FLOAT,
            temperature_measured FLOAT,
            voltage_charge FLOAT,
            time FLOAT,
            power FLOAT,
            soc FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        """
        with self.connection.cursor() as cursor:
            cursor.execute(create_table_query)
        self.connection.commit()
        logger.info("Table created")
        
    def insert_prediction(self, voltage_measured, current_measured, temperature_measured, voltage_charge, time, power, soc):
        insert_query = """
        INSERT INTO predictions (voltage_measured, current_measured, temperature_measured, voltage_charge, time, power, soc)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        with self.connection.cursor() as cursor:
            cursor.execute(insert_query, (voltage_measured, current_measured, temperature_measured, voltage_charge, time, power, soc))
        self.connection.commit()
        logger.info("Prediction inserted")
    
    def close(self):
        if self.connection:
            self.connection.close()
            logger.info("Connection closed")
    
        