from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

hostname = os.environ.get("SERVER")
database = os.environ.get("DATABASE")
username = os.environ.get("POSTGRES_USER")
password = os.environ.get("PASSWORD")
# print(hostname, database, username, password)


# Create connection string
connection_string = f"postgresql://{username}:{password}@{hostname}/{database}"

# Create SQLAlchemy engine
engine = create_engine(connection_string)

# Execute SQL query and retrieve data into a DataFrame
query = "SELECT * FROM Reviews;"
df = pd.read_sql(query, engine)

# Display the DataFrame
print(df.head())