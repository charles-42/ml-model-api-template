import pandas as pd
from sqlalchemy import create_engine

resourceGroupName="BENIAC_data_api_olist"
location="francecentral" 
serverName="DBOlistModelApiTemplate"
databaseName="olist"
username="adminuser"
password='eyJhbGciOiJIUzI1NiIsInR5cCI@^zdW%IiOiJhZG1pbiH3CxlTRDJj3RMKrY6B4x8'
table= 'Rewiews'

# Define the connection string
connection_string = f'mssql+pyodbc://{username}:{password}@{serverName}.database.windows.net/{databaseName}?driver=ODBC+Driver+17+for+SQL+Server'

# Create the SQLAlchemy engine
engine = create_engine(connection_string)

# Define the SELECT query
query = f'SELECT * FROM {table}'

# Execute the query and load the results into a pandas DataFrame
df = pd.read_sql(query, engine)

# Display the DataFrame
print(df)