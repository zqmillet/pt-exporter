from typing import Dict
from argparse import ArgumentParser

from fastapi import FastAPI
from fastapi import Response
from uvicorn import run
from prometheus_client import generate_latest
from prometheus_client import CollectorRegistry
from prometheus_client import Gauge
from apscheduler.schedulers.background import BackgroundScheduler # type: ignore
from loguru import logger

from .crawlers import Crawlers

parser = ArgumentParser()
parser.add_argument(
    '-p', '--port',
    type=int,
    default=8000,
    help='port of the server'
)

parser.add_argument(
    '--host',
    type=str,
    default='0.0.0.0',
    help='ip address for listening'
)

parser.add_argument(
    '-c', '--configuration-file-path',
    type=str,
    required=True,
    help='path of the configuration file'
)

arguments = parser.parse_args()

application = FastAPI()

registry = CollectorRegistry()

upload_bytes_gauge = Gauge('upload_bytes', 'upload bytes of website', ['website'], registry=registry)
download_bytes_gauge = Gauge('download_bytes', 'download bytes of website', ['website'], registry=registry)
bonus_gauge = Gauge('bonus', 'download bytes of website', ['website'], registry=registry)

upload_bytes_group: Dict[str, int] = {}
download_bytes_group: Dict[str, int] = {}
bonus_group: Dict[str, float] = {}

crawlers = Crawlers(arguments.configuration_file_path, logger) # type: ignore

@application.get('/metrics')
def metrics():
    return Response(generate_latest(registry), media_type='text/plain')

def get_headers(file_path: str) -> Dict[str, str]:
    headers = {}
    with open(file_path, 'r', encoding='utf8') as file:
        for line in file:
            key, value = line.strip().split(': ')
            headers[key] = value.strip()
    return headers

def update_data():
    for website, user in crawlers.get_users().items():
        upload_bytes_gauge.labels(website).set(user.upload_bytes)
        download_bytes_gauge.labels(website).set(user.download_bytes)
        bonus_gauge.labels(website).set(user.bonus)

scheduler = BackgroundScheduler()
scheduler.add_job(update_data, 'interval', minutes=30)
scheduler.start()

update_data()

def main():
    run(application, host=arguments.host, port=arguments.port)

if __name__ == '__main__':
    main()
