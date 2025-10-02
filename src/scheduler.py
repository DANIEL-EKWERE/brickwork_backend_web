import sys
import json
import downloader
import ingestion as ingestion
from datetime import datetime, timedelta
from constants import ROOT_DIR, LAST_RUN_FILE_NAME

from common import upload_object_to_s3, download_object_from_s3

from database import upload_db, download_db


FUNCTION_MAPPING = {"downloader": downloader.main, "integration_service": ingestion.main}

# Intervals for each service in days or specific weekdays
INTERVALS = {
    "downloader": 2,  # run every two days
    "integration_service": {0, 2, 5},  # 0=Monday, 2=Wednesday, 5=Saturday
}


def load_last_run_data():
    data = download_object_from_s3(LAST_RUN_FILE_NAME)

    if data:
        return json.loads(data)

    last_run_path = ROOT_DIR / LAST_RUN_FILE_NAME
    if last_run_path.exists():
        return json.loads(last_run_path.read_text())
    else:
        return {}


def save_last_run_data(last_run_data):
    last_run_path = ROOT_DIR / LAST_RUN_FILE_NAME
    with last_run_path.open("w") as f:
        json.dump(last_run_data, f, indent=4)
    upload_object_to_s3(object=json.dumps(last_run_data), s3_file_name=LAST_RUN_FILE_NAME)


def should_run_today(service, last_run_data):
    now = datetime.now()
    if isinstance(INTERVALS[service], set):
        # Service is scheduled for specific weekdays
        if now.weekday() in INTERVALS[service]:
            return True
    else:
        # Service runs every n days
        next_run_time = last_run_data.get(service, {}).get("next_run_time", "")
        if next_run_time:
            next_run_time = datetime.strptime(next_run_time, "%Y-%m-%d %H:%M:%S")
            return now >= next_run_time
        return True  # Run if no last run time
    return False


def run_function(func):
    func()


def schedule_functions(force=False):
    last_run_data = load_last_run_data()
    now = datetime.now()

    for service, func in FUNCTION_MAPPING.items():
        if force or should_run_today(service, last_run_data):
            print(f"Running {service}")
            try:
                func()
                # Update last run time to now
                last_run_data[service] = {
                    "last_run_time": now.strftime("%Y-%m-%d %H:%M:%S"),
                    "next_run_time": (
                        now + timedelta(days=INTERVALS.get(service, 1) if isinstance(INTERVALS[service], int) else 1)
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                }
                save_last_run_data(last_run_data)

            except Exception as e:
                print(f"Error running {service}: {e}")


def main():
    force = False

    if len(sys.argv) > 1 and sys.argv[1] == "-f":
        force = True

    print("Starting scheduler")
    download_db()
    schedule_functions(force)
    upload_db()
    print("scheduler(): scheduler service complete...")
    print("Scheduler finished")


if __name__ == "__main__":
    main()
