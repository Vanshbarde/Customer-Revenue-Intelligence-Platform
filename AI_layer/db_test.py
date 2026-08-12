from db import DatabaseManager

db = DatabaseManager()

db.connect()

df = db.get_view_data(
    "vw_executive_dashboard"
)

print(df)

db.disconnect()