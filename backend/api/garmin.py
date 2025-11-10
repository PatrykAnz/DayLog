from garminconnect import Garmin
import os
from datetime import date, timedelta
from database.database import init_db, insert_data  
from auth.azure_auth import azure_auth
#YEAR MONTH DAY
START_DATE = date(2025, 6, 1)

GARMIN_EMAIL, GARMIN_PASSWORD = azure_auth("garmin-email","garmin-password")
def init_client():
    client = Garmin(
        GARMIN_EMAIL,
        GARMIN_PASSWORD
    )
    client.login()
    print(client)
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


def sync_yesterday():
    client = init_client()
    conn, cur = init_db()
    yesterday = date.today() - timedelta(days=1)
    data = fetch_day_data(client, yesterday.isoformat())
    insert_data(cur, conn, data)
    print(f"Inserted yesterday: {yesterday}")
    cur.close()
    conn.close()


def sync_year():
    client = init_client()
    conn, cur = init_db()
    today = date.today()

    for i in range((today - START_DATE).days + 1):
        day = START_DATE + timedelta(days=i)
        if i % 10 == 0:
            print(f"{i} days done")
        data = fetch_day_data(client, day.isoformat())
        insert_data(cur, conn, data)
    print("Inserted yearly data")
    cur.close()
    conn.close()


if __name__ == "__main__":
    sync_yesterday()
    print(sync_yesterday())
    pass
