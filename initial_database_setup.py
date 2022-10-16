# WARNING: DO NOT RUN THIS FILE

import psycopg2
import pandas as pd

# Note: Regenerate Password In "test_password.txt" Before Use
password = open("test files/test_password.txt", "r").read()
#password = open("hidden files/real_password.txt", "r").read()

conn = psycopg2.connect(f"postgresql://foodle-admin:{password}@free-tier9.gcp-us-west2.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dfoodle-1453")
cur = conn.cursor()


# Create Empty Tables for data
cur.execute("""
    CREATE TABLE people.data (
    user_id STRING,
    date STRING,
    sex STRING,
    age INT,
    height DECIMAL,
    weight DECIMAL,
    caloric_intake DECIMAL,
    protein_grams_intake DECIMAL,
    carb_grams_intake DECIMAL,
    fat_grams_intake DECIMAL
    )
""")
cur.execute("""
    CREATE TABLE people.names (
    user_id STRING,
    name STRING
    );
""")
conn.commit()


# Create Nutrients Table
cur.execute("""
    CREATE TABLE nutrients.data (
    food STRING,
    measure STRING,
    grams DECIMAL,
    calories DECIMAL,
    protein DECIMAL,
    fat DECIMAL,
    sat_fat DECIMAL,
    fiber DECIMAL,
    carbs DECIMAL,
    category STRING
    )
""")
data = pd.read_csv (r'nutrients_csvfile.csv')
df = pd.DataFrame(data)
for row in df.itertuples():
    cur.execute(f"""
        INSERT INTO nutrients.data
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (row.Food, row.Measure, row.Grams, row.Calories, row.Protein, row.Fat, row.Sat_Fat, row.Fiber, row.Carbs, row.Category))
conn.commit()
cur.close()
