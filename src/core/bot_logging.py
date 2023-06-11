import logging

logging.basicConfig(
    filename="bot.log", 
    filemode="w",
    encoding="utf-8",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='[%Y/%m/%d %H:%M:%S]'
)
