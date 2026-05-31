import time
import schedule
from datetime import datetime
import subprocess

# ---------------------------------------------------

# RUN PIPELINE

# ---------------------------------------------------

def run_pipeline():


print("\n--------------------------------")
print("STARTING AUTOMATION PIPELINE")
print("--------------------------------")

print(
    f"Time: {datetime.now()}"
)

try:

    subprocess.run(
        ["python", "main.py"],
        check=True
    )

    print(
        "\nPipeline completed successfully"
    )

except Exception as e:

    print("\nPipeline failed")
    print(e)


# ---------------------------------------------------

# SCHEDULE TIMES

# ---------------------------------------------------

# Best Shorts timings (India)

schedule.every().day.at(
"07:00"
).do(run_pipeline)

schedule.every().day.at(
"13:00"
).do(run_pipeline)

schedule.every().day.at(
"19:00"
).do(run_pipeline)

# ---------------------------------------------------

# LOOP

# ---------------------------------------------------

print("\nScheduler started...")

while True:


schedule.run_pending()

time.sleep(10)

