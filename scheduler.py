import schedule
import time
import os

def run_job():
    os.system("python scraper.py")

schedule.every().day.at("02:38").do(run_job)

print("Scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(60)
