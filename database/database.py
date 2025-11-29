import psycopg2
import os
from auth.azure_auth import get_secret

def init_db():
    db_name = "app"
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
    cur.execute("""
            CREATE TABLE IF NOT EXISTS withings (
                date DATE PRIMARY KEY,
                weight_kg FLOAT,
                fat_free_mass_kg FLOAT,
                fat_ratio_percent FLOAT,
                fat_mass_kg FLOAT,
                muscle_mass_kg FLOAT,
                hydration_kg FLOAT,
                bone_mass_kg FLOAT
        )
    """)
    conn.commit()
    return conn, cur


def insert_data_garmin(cur, conn, data):
    cur.execute("""
        INSERT INTO garmin VALUES (
            %(date)s, %(total_steps)s, %(total_sleep_seconds)s,
            %(deep_sleep_seconds)s, %(light_sleep_seconds)s, %(rem_sleep_seconds)s, %(awake_sleep_seconds)s,
            %(min_hr)s, %(rest_hr)s, %(last7_avg_rest_hr)s, %(avg_stress)s, %(stress_duration)s,
            %(avg_spo2)s, %(min_spo2)s, %(last7_avg_spo2)s, %(avg_sleep_resp)s, %(avg_waking_resp)s,
            %(body_battery_most_recent)s, %(body_battery_at_wake)s, %(body_battery_lowest)s
        )
        ON CONFLICT (date) DO UPDATE SET
            total_steps = EXCLUDED.total_steps,
            total_sleep_seconds = EXCLUDED.total_sleep_seconds,
            deep_sleep_seconds = EXCLUDED.deep_sleep_seconds,
            light_sleep_seconds = EXCLUDED.light_sleep_seconds,
            rem_sleep_seconds = EXCLUDED.rem_sleep_seconds,
            awake_sleep_seconds = EXCLUDED.awake_sleep_seconds,
            min_hr = EXCLUDED.min_hr,
            rest_hr = EXCLUDED.rest_hr,
            last7_avg_rest_hr = EXCLUDED.last7_avg_rest_hr,
            avg_stress = EXCLUDED.avg_stress,
            stress_duration = EXCLUDED.stress_duration,
            avg_spo2 = EXCLUDED.avg_spo2,
            min_spo2 = EXCLUDED.min_spo2,
            last7_avg_spo2 = EXCLUDED.last7_avg_spo2,
            avg_sleep_resp = EXCLUDED.avg_sleep_resp,
            avg_waking_resp = EXCLUDED.avg_waking_resp,
            body_battery_most_recent = EXCLUDED.body_battery_most_recent,
            body_battery_at_wake = EXCLUDED.body_battery_at_wake,
            body_battery_lowest = EXCLUDED.body_battery_lowest
    """, data)
    conn.commit()


def insert_data_withings(cur, conn, data):
    cur.execute("""
        INSERT INTO withings VALUES (
            %(date)s, %(weight_kg)s, %(fat_free_mass_kg)s, %(fat_ratio_percent)s,
            %(fat_mass_kg)s, %(muscle_mass_kg)s, %(hydration_kg)s, %(bone_mass_kg)s
        )
        ON CONFLICT (date) DO UPDATE SET
            weight_kg = EXCLUDED.weight_kg,
            fat_free_mass_kg = EXCLUDED.fat_free_mass_kg,
            fat_ratio_percent = EXCLUDED.fat_ratio_percent,
            fat_mass_kg = EXCLUDED.fat_mass_kg,
            muscle_mass_kg = EXCLUDED.muscle_mass_kg,
            hydration_kg = EXCLUDED.hydration_kg,
            bone_mass_kg = EXCLUDED.bone_mass_kg
    """, data)
    conn.commit()
