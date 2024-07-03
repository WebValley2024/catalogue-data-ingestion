from eq import get_eq
from swe import get_swe
from tgf import get_tgf
from grb import get_grb
from gms import get_gms
import threading
from sqlalchemy import create_engine
import pandas as pd
import os

from rich.console import Console
from rich.progress import Progress
from rich import print
from time import strftime, localtime

console = Console()


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
    with Progress() as progress:
        download_task = progress.add_task("[green]Downloading data...", total=5)

        threads = []
        threads.append(threading.Thread(target=lambda: [thread_get_eq(), progress.advance(download_task)]))
        threads.append(threading.Thread(target=lambda: [thread_get_swe(), progress.advance(download_task)]))
        threads.append(threading.Thread(target=lambda: [thread_get_tgf(), progress.advance(download_task)]))
        threads.append(threading.Thread(target=lambda: [thread_get_grb(), progress.advance(download_task)]))
        threads.append(threading.Thread(target=lambda: [thread_get_gms(), progress.advance(download_task)]))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        if not progress.finished:
            progress.stop()