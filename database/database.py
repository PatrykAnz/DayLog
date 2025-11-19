import psycopg2
import os
from auth.azure_auth import get_secret

def init_db():
    db_name = "daylog-database"
    db_user = get_secret("daylog-db-username")
    db_password = get_secret("daylog-db-password")
    db_host = os.environ.get("DB_HOST", "daylog-db-cnpg-rw.daylog.svc.cluster.local")
    db_port = "5432"
    
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    cur = conn.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS garmin (
                date DATE PRIMARY KEY,
                total_steps INT,
                total_sleep_seconds INT,
                deep_sleep_seconds INT,
                light_sleep_seconds INT,
                rem_sleep_seconds INT,
                awake_sleep_seconds INT,
                min_hr INT,
                rest_hr INT,
                last7_avg_rest_hr INT,
                avg_stress INT,
                stress_duration INT,
                avg_spo2 FLOAT,
                min_spo2 FLOAT,
                last7_avg_spo2 FLOAT,
                avg_sleep_resp FLOAT,
                avg_waking_resp FLOAT,
                body_battery_most_recent INT,
                body_battery_at_wake INT,
                body_battery_lowest INT
        )
    """)
    conn.commit()
    return conn, cur


def insert_data(cur, conn, data):
    cur.execute("""
        INSERT INTO garmin VALUES (
            %(date)s, %(total_steps)s, %(total_sleep_seconds)s,
            %(deep_sleep_seconds)s, %(light_sleep_seconds)s, %(rem_sleep_seconds)s, %(awake_sleep_seconds)s,
            %(min_hr)s, %(rest_hr)s, %(last7_avg_rest_hr)s, %(avg_stress)s, %(stress_duration)s,
            %(avg_spo2)s, %(min_spo2)s, %(last7_avg_spo2)s, %(avg_sleep_resp)s, %(avg_waking_resp)s,
            %(body_battery_most_recent)s, %(body_battery_at_wake)s, %(body_battery_lowest)s
        )
        ON CONFLICT (date) DO NOTHING
    """, data)
    conn.commit()
