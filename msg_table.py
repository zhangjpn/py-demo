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

    def serve(self, msg_handler):
        while 1:
            time.sleep(10)


class Message(object):
    pass
    def get_id(self):
        raise NotImplementedError

    def to_dict(self):
        return dict(self.__dict__)

    def encode(self):

        return {'message': self.__class__.__name__, 'params': self.to_dict(), 'id': self.get_id()}


class Command(Message):
    pass


class Event(Message):
    pass


class ConfirmFee(Command):
    """结算费用"""

    def __init__(self, tid, order_id):
        self.tid = tid
        self.order_id = order_id


class FeeConfirmed(Event):
    """费用已经被结算成功"""

    def __init__(self, tid, order_id):
        self.tid = tid
        self.order_id = order_id


class LocalMsgTable(object):

    def prepare(self, tran, msg):
        """添加消息到本地消息表"""
        tran.insert(msg)

    def confirm(self, msg):
        """确认消息成功"""

    def serve(self, msg_dispatcher):
        """监控本地消息表，定时轮询"""
        while 1:
            msg_list = self.get_all_msg()
            for msg in msg_list:
                msg_dispatcher.send(msg)

    def get_all_msg(self):
        """获取"""
        sql = '''select * from msg_table where status = `init` '''
        return [{}, {}]


@contextlib.contextmanager
def trans():
    yield 'tran'


def do_some_work(tran):
    pass


main_producer = QueueProducer()
main_consumer = QueueConsumer()

slave_producer = QueueProducer()
slave_consumer = QueueConsumer()


def main_service():
    # start trans
    table = LocalMsgTable()

    msg = {}

    with trans as tran:
        do_some_work(tran)
        table.prepare(tran=tran, msg=msg)  # 记录一个必要做的事情，放在事务内保证了任务与其它事务保持一致，不会丢失
    main_producer.send(msg=msg)  # 通知一个必要做的事，这种重要的事情应该以命令的形式发起，即没有回滚可言，下游必须成功执行


def main_compensate():
    """此处是为了重发消息，保证下游服务必须执行，否则会不断重发"""
    table = LocalMsgTable()
    table.serve(main_producer)


def main_listener():
    """监控并更新最新的"""

    def handler(msg):
        table = LocalMsgTable()
        table.confirm(msg)  # 此处订阅消息队列，如果命令已经得到正确执行，则将任务改成已经执行成功，后续不需要再去触发

    main_consumer.serve(handler)


def slave_service():
    """从服务负责另外的一些代码，通过命令的方式触发，并在完成后广播一个事件，告诉触发者，工作已经完成"""

    def msg_handler(msg):
        # 由于可能会同一条消息收到多次，所以必须保证幂等性
        print(f'slave handle msg: {msg}')
        success_msg = {}
        slave_producer.send(success_msg)

    slave_consumer.serve(msg_handler)
