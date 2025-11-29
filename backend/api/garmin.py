import os
import logging
from garminconnect import Garmin
from datetime import date, timedelta
from database.database import init_db, insert_data_garmin
from auth.azure_auth import azure_auth

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger("garmin")
log.setLevel(logging.INFO)

START_DATE = date(2024, 6, 1)

def init_client():
    garmin_email, garmin_password = azure_auth("garmin-email", "garmin-password")
    client = Garmin(garmin_email, garmin_password)
    client.login()
    return client


def fetch_day_data(client, day_str):
    stats = client.get_stats(day_str)
    spo2 = client.get_spo2_data(day_str)
    respiration = client.get_respiration_data(day_str)
    sleep = client.get_sleep_data(day_str)

    return {
        "date": day_str,
        "total_steps": stats.get("totalSteps"),
        "total_sleep_seconds": stats.get("sleepingSeconds"),
        "deep_sleep_seconds": sleep.get("dailySleepDTO", {}).get("deepSleepSeconds"),
        "light_sleep_seconds": sleep.get("dailySleepDTO", {}).get("lightSleepSeconds"),
        "rem_sleep_seconds": sleep.get("dailySleepDTO", {}).get("remSleepSeconds"),
        "awake_sleep_seconds": sleep.get("dailySleepDTO", {}).get("awakeSleepSeconds"),
        "min_hr": stats.get("minHeartRate"),
        "rest_hr": stats.get("restingHeartRate"),
        "last7_avg_rest_hr": stats.get("lastSevenDaysAvgRestingHeartRate"),
        "avg_stress": stats.get("averageStressLevel"),
        "stress_duration": stats.get("stressDuration"),
        "avg_spo2": spo2.get("averageSpO2"),
        "min_spo2": spo2.get("lowestSpO2"),
        "last7_avg_spo2": spo2.get("lastSevenDaysAvgSpO2"),
        "avg_sleep_resp": respiration.get("avgSleepRespirationValue"),
        "avg_waking_resp": respiration.get("avgWakingRespirationValue"),
        "body_battery_most_recent": stats.get("bodyBatteryMostRecentValue"),
        "body_battery_at_wake": stats.get("bodyBatteryAtWakeTime"),
        "body_battery_lowest": stats.get("bodyBatteryLowestValue"),
    }


def sync_last_7_days():
    client = init_client()
    conn, cur = init_db()
    today = date.today()
    total_days = 7
    for i in range(1, total_days + 1):
        day = today - timedelta(days=i)
        data = fetch_day_data(client, day.isoformat())
        if data.get("total_steps") is None and data.get("total_sleep_seconds") is None:
            continue
        insert_data_garmin(cur, conn, data)
        if (i) % 2 == 0 or (i) == total_days:
            log.info(f"synced {i}/{total_days} days")
    cur.close()
    conn.close()


def sync_year():
    client = init_client()
    conn, cur = init_db()
    today = date.today()
    total_days = (today - START_DATE).days + 1
    
    for i in range(total_days):
        day = START_DATE + timedelta(days=i)
        data = fetch_day_data(client, day.isoformat())
        if data.get("total_steps") is None and data.get("total_sleep_seconds") is None:
            continue
        insert_data_garmin(cur, conn, data)
        if (i + 1) % 10 == 0 or (i + 1) == total_days:
            log.info(f"synced {i + 1}/{total_days} days")
    cur.close()
    conn.close()


if __name__ == "__main__":
    sync_mode = os.environ.get("SYNC_MODE", "last_7_days")
    if sync_mode == "year":
        sync_year()
    else:
        sync_last_7_days()
