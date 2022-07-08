"""本地消息表"""

# 解决的问题：基于消息的分布式事务最终一致性方案
import contextlib
import time


class QueueProducer(object):
    def send(self, msg):
        print(f'send msg: {msg} to queue')


class QueueConsumer(object):

    def consume(self, msg):
        print(f'consume msg: {msg}')

    def start(self):
        pass

    def serve(self):
        while 1:
            time.sleep(10)


class LocalMsgTable(object):

    def add_msg(self, msg):
        """添加消息到本地消息表"""
        pass

    def monitor_loop(self, gap=10):
        """监控本地消息表，定时轮询"""
        producer = QueueProducer()
        while 1:
            msg = self.get_unfinished_msg()
            producer.send(msg)

    def get_unfinished_msg(self):
        """获取"""
        sql = '''select * from msg_table where status = `init` '''
        return [{}, {}]


@contextlib.contextmanager
def trans():
    yield 'tran'


def do_some_work(tran):
    pass


def main_task():
    # start trans
    table = LocalMsgTable()
    producer = QueueProducer()
    msg = {}

    with trans as tran:
        do_some_work(tran)
        table.add_msg(msg)
    producer.send(msg)


def down_stream_service():
    consumer = QueueConsumer()
    consumer.serve()


def compensate():
    table = LocalMsgTable()
    table.monitor_loop(gap=10)
