import random
import time


def hash(qq: int):
    # days = int(time.strftime("%d", time.localtime(time.time()))) + 31 * int(
    #     time.strftime("%m", time.localtime(time.time()))) + 55
    day = int(time.strftime("%d", time.localtime(time.time()))) + 4
    month = int(time.strftime("%m", time.localtime(time.time())))
    year = int(time.strftime("%y", time.localtime(time.time())))
    days = ((day + 11) * year // month + month * 31) * (year - day + 23)
    return (days * qq) >> 8


def getRandom(num: int) -> int :
    return random.randint(1,num) % num
