-- Create table Orders
IF object_id('Orders', 'U') is null
    CREATE TABLE Orders (
        order_id VARCHAR(64) PRIMARY KEY,
        customer_id VARCHAR(64),
        order_status VARCHAR(64),
        order_purchase_timestamp DATETIME2,
        order_approved_at DATETIME2,
        order_delivered_carrier_date DATETIME2,
        order_delivered_customer_date DATETIME2,
        order_estimated_delivery_date DATETIME2,
    );
ELSE
    PRINT 'Orders exists already'


IF object_id('Reviews', 'U') is null
    CREATE TABLE Reviews (
        review_id VARCHAR(64) PRIMARY KEY,
        order_id VARCHAR(64),
        review_score INT,
        review_comment_title VARCHAR(64),
        review_comment_message VARCHAR(600),
        review_creation_date DATETIME2,
        review_answer_timestamp DATETIME2,
        FOREIGN KEY (order_id) REFERENCES Orders(order_id)
    );
ELSE
    PRINT 'Reviews exists already'

