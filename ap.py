
"""测试apscheduler任务丢失的问题"""

from apscheduler.triggers.cron import CronTrigger
from kazoo.client import KazooClient
import pymongo
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime

from kazoo.client import KazooState

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# def my_listener(state):
#     if state == KazooState.LOST:
#         # Register somewhere that the session was lost
#     elif state == KazooState.SUSPENDED:
#         # Handle being disconnected from Zookeeper
#     else:
#         # Handle being connected/reconnected to Zookeeper



zk = KazooClient()


def do_something():
    now = datetime.now()
    logger.info(f'>>> Now is at {now}')

@zk.DataWatch("/my/favorite")
def on_conf_update(data, stat):
    logger.info(f'Config updated: data: {data}, stat: {stat}')
    conf = data.decode(encoding='utf-8')
    set_job(conf)

mongostore = MongoDBJobStore(
        host='127.0.0.1',
        port=27017,
        database='jobs',
        collection="jobs",
    )
scheduler = BlockingScheduler(
    logger=logger,
    jobstores={"default": mongostore},
    executors={"default": ThreadPoolExecutor(20)},
    job_defaults={"coalesce": True, "max_instances": 3},
    timezone='Asia/Shanghai',
)

def set_job(conf):
    tg = CronTrigger.from_crontab(conf)
    scheduler.add_job(do_something,
                      trigger=tg,
                      id="AJOB",
                      replace_existing=True,
                      misfire_grace_time=3600)



zk.start()

logger.info('Scheduler Started.')
scheduler.start()
