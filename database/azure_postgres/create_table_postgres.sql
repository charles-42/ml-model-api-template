-- Create table Orders
CREATE TABLE IF NOT EXISTS  Orders (
        order_id VARCHAR(64) PRIMARY KEY,
        customer_id VARCHAR(64),
        order_status VARCHAR(64),
        order_purchase_timestamp TIMESTAMP,
        order_approved_at TIMESTAMP,
        order_delivered_carrier_date TIMESTAMP,
        order_delivered_customer_date TIMESTAMP,
        order_estimated_delivery_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS  Reviews (
        review_id VARCHAR(64) PRIMARY KEY,
        order_id VARCHAR(64),
        review_score INT,
        review_comment_title VARCHAR(64),
        review_creation_date TIMESTAMP,
        review_answer_timestamp TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);