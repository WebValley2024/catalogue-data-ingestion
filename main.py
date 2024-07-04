from eq import get_eq
from swe import get_swe
from tgf import get_tgf
from grb import get_grb
from gms import get_gms
import threading
from sqlalchemy import create_engine
import pandas as pd
import os

from time import strftime, localtime

def thread_get_eq():
    get_eq()
    print("<eq> Download completed.")


def thread_get_swe():
    get_swe()
    print("<swe> Download completed.")


def thread_get_tgf():
    get_tgf()
    print("<tgf> Download completed.")


def thread_get_grb():
    get_grb()
    print("<grb> Download completed.")


def thread_get_gms():
    get_gms()
    print("<gms> Download completed.")


if __name__ == "__main__":
    threads = []
    threads.append(threading.Thread(target=lambda: [thread_get_eq()]))
    threads.append(threading.Thread(target=lambda: [thread_get_swe()]))
    threads.append(threading.Thread(target=lambda: [thread_get_tgf()]))
    threads.append(threading.Thread(target=lambda: [thread_get_grb()]))
    threads.append(threading.Thread(target=lambda: [thread_get_gms()]))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
