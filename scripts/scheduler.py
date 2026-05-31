import time
import schedule
import traceback

from main import run_pipeline

UPLOAD_TIMES = [

    "08:00",
    "13:00",
    "19:00",
    "22:00"
]

def safe_run():

    try:

        print("\nStarting scheduled upload...\n")

        run_pipeline()

    except Exception as e:

        print("\nScheduled upload failed")

        print(e)

        traceback.print_exc()

for upload_time in UPLOAD_TIMES:

    schedule.every().day.at(
        upload_time
    ).do(safe_run)

print("\nScheduler started...\n")

while True:

    schedule.run_pending()

    time.sleep(20)