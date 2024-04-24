import pandas as pd
import sqlite3
connection = sqlite3.connect("olist.db")

review_query = """
SELECT * 
FROM REVIEWS
"""

df_reviews = pd.read_sql_query(review_query, connection)

df_reviews = df_reviews.drop(['review_comment_message','timestamp_field_7'], axis=1)
df_reviews.review_creation_date = pd.to_datetime(df_reviews['review_creation_date'], format= '%Y-%m-%d %H:%M:%S', errors="coerce")
df_reviews.review_answer_timestamp = pd.to_datetime(df_reviews['review_answer_timestamp'], format= '%Y-%m-%d %H:%M:%S', errors="coerce")


df_reviews.to_csv("reviews.csv", index=False)
