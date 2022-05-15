from apscheduler.schedulers.background import BackgroundScheduler
from .views import updateWeather

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(updateWeather, 'interval', seconds=60)
    scheduler.start()