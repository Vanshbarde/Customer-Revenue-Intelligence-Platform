import psycopg2
import pandas as pd

from config import DB_CONFIG


class DatabaseManager:

    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            print("✅ PostgreSQL Connected")
        except Exception as e:
            print(f"❌ Connection Error: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("🔒 Connection Closed")

    def get_dataframe(self, query):

        try:
            df = pd.read_sql_query(
                query,
                self.connection
            )
            return df

        except Exception as e:
            print(f"❌ Query Error: {e}")
            return None

    def get_view_data(self, view_name):

        query = f"""
        SELECT *
        FROM {view_name}
        """

        return self.get_dataframe(query)