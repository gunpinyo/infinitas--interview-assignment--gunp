import logging
import sys

import yaml
import pandas as pd
import pandasql
import psycopg2
from psycopg2.extras import LoggingConnection

def main():
    with (open("../config.yaml", "rt", encoding="utf-8") as config_file,
          open("../secret.yaml", "rt", encoding="utf-8") as secret_file):
        config_data = yaml.safe_load(config_file)
        secret_data = yaml.safe_load(secret_file)

        db_settings = {
            "database": "postgres",
            "host": "postgres",
            "user": secret_data["postgres-username"],
            "password": secret_data["postgres-password"],
            "port": "5432",
        }
    
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.StreamHandler(sys.stdout))
    
        conn = psycopg2.connect(
            connection_factory=LoggingConnection,
            **db_settings)
        conn.initialize(logger)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS events RESTRICT")
        # cursor.execute("""CREATE TABLE events (
        # 
        #                   );""")
        # rows = cursor.fetchall()
        # for row in rows:
        #     print(row)
        conn.commit()
        conn.close()


if __name__ == '__main__':
    main()
