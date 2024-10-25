from typing import Dict
from typing import List

from fastapi import FastAPI
from fastapi import Response
from uvicorn import run
from prometheus_client import generate_latest
from prometheus_client import CollectorRegistry
from prometheus_client import Gauge
from apscheduler.schedulers.background import BackgroundScheduler
from crawlers import MTeam
from crawlers import Crawler
from loguru import logger

application = FastAPI()

registry = CollectorRegistry()
gauge = Gauge('upload_bytes', 'upload bytes of website', ['website'], registry=registry)

uploads: Dict[str, int] = {}

@application.get('/metrics')
def metrics():
    for website, upload_bytes in uploads.items():
        gauge.labels(website=website).set(upload_bytes)

    return Response(generate_latest(registry), media_type='text/plain')

def get_headers(file_path: str) -> Dict[str, str]:
    headers = {}
    with open(file_path, 'r', encoding='utf8') as file:
        for line in file:
            key, value = line.strip().split(': ')
            headers[key] = value.strip()
    return headers

mteam = MTeam(get_headers('./headers/mteam.header'))
crawlers: List[Crawler] = [mteam]

def update_data():
    for crawler in crawlers:
        try:
            user = crawler.get_user()
        except Exception as exception:
            logger.exception(exception)
        else:
            uploads[crawler.__class__.__name__] = user.upload_bytes
            logger.info(f'update {crawler.__class__.__name__} data')

scheduler = BackgroundScheduler()
scheduler.add_job(update_data, 'interval', minutes=5)
scheduler.start()

update_data()

if __name__ == '__main__':
    run(application, host='0.0.0.0', port=1926)
