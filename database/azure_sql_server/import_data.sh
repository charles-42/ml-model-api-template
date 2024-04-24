# Azure SQL Server credentials
server="DBOlistModelApiTemplate.database.windows.net"
database="olist"
username="adminuser"
password="eyJhbGciOiJIUzI1NiIsInR5cCI@^zdW%IiOiJhZG1pbiH3CxlTRDJj3RMKrY6B4x8"

# # Path to your CSV file
# csvFileOrders="/Users/charles/Documents/pythonProject/data-model-template/data/orders_dataset.csv"

# # Import data
# bcp Orders in $csvFileOrders -S $server -d $database -U $username -P $password -q -c -t ","

# Path to your CSV file
csvFileReviews="./data/reviews_dataset.csv"

# Import data
bcp Reviews in $csvFileReviews -S $server -d $database -U $username -P $password -q -c -t ","


# # Path to your SQL script file
# sqlScript="/Users/charles/Documents/pythonProject/data-model-template/azure_db_building/import_orders.sql"

# # Connect to Azure SQL Server and execute the SQL script
# sqlcmd -S $server -d $database -U $username -P $password -i $sqlScript


# # Path to your CSV file
# csvFileOrders="/Users/charles/Documents/pythonProject/data-model-template/data/orders_dataset.csv"

# # Define the SQL query to perform the import
# sqlQueryOrders="BULK INSERT Orders FROM '$csvFileOrders' WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n', FIRSTROW = 2)"

# echo $pwd
# pwd
# # Connect to Azure SQL Server and execute the SQL query
# sudo sqlcmd -S $server -d $database -U $username -P $password -Q "$sqlQueryOrders"

# # Path to your CSV file
# csvFileReviews="./data/olist_order_reviews_dataset.csv"

# # Define the SQL query to perform the import
# sqlQueryReviews="BULK INSERT Reviews FROM '$csvFileReviews' WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n', FIRSTROW = 2)"

# # Connect to Azure SQL Server and execute the SQL query
# sqlcmd -S $server -d $database -U $username -P $password -Q "$sqlQueryReviews"