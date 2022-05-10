from models import bot
import time

bot.accelerate(30)
bot.turn(100)
time.sleep(8)

bot.stop()