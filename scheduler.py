import schedule
import time
import threading
from config import VOTE_DURATION
from bot import bot

def daily_vote():
    print("[SCHEDULER] Щоденне голосування (шаблон)")

def weekly_titles():
    bot.send_message(316531557, "🏆 Титули тижня ще не реалізовані — шаблон")

schedule.every().day.at("19:00").do(daily_vote)
schedule.every().sunday.at("12:00").do(weekly_titles)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=run_scheduler).start()
