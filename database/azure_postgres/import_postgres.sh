# Load environment variables from .env file
set -o allexport
source .env
set +o allexport

orderscsv="/Users/charles/Documents/pythonProject/data-model-template/database/data/orders_dataset.csv"
reviewscsv="/Users/charles/Documents/pythonProject/data-model-template/database/data/reviews_dataset.csv"

# Connect to Azure SQL Server and execute the SQL script
export PGPASSWORD=$PASSWORD 
psql -h $SERVER -d $DATABASE -U $POSTGRES_USER -c"\copy Orders FROM '$orderscsv' DELIMITER ',' CSV HEADER;"
psql -h $SERVER -d $DATABASE -U $POSTGRES_USER -c"\copy Reviews FROM '$reviewscsv' DELIMITER ',' CSV HEADER;"
