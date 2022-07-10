# -*- coding:utf-8 -*-


class QueueProducer(object):
    def send(self, msg):
        print(f'send msg: {msg} to queue')


class QueueConsumer(object):

    def __init__(self):
        self.handler = None

    def connect(self):
        """连接消息队列"""

    def start(self):
        pass

    def set_handler(self, handler):
        self.handler = handler

    def serve(self):
        self.connect()
        while 1:
            msg = self.get_msg()
            self.handler(msg)

    def get_msg(self):
        return {}
