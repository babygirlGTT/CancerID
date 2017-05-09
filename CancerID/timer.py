from datetime import time, timedelta, datetime 
import schedule
EXTRACT_PERIOD = 30 #seconds
MODEL_UPDATE_PERIOD = 1 #day

def job1():
    print("I'm working on job1...")

def job2()：
    print("I'm working on job2...")
schedule.every(EXTRACT_PERIOD).seconds.do(job)
# schedule.every().day("10:30").do(job)
schedule.every(MODEL_UPDATE_PERIOD).day().do(job)

while 1:
    schedule.run_pending()
