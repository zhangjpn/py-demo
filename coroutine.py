# -*- coding:utf-8 -*-

import inspect
from pprint import pprint


def gen(ident):
    """生成器函数"""
    print('开启', ident)
    yield f'yield 返回值{ident}'
    print('准备返回', ident)
    return f'返回值{ident}'


print(inspect.isgenerator(gen(1)))
print(inspect.isgeneratorfunction(gen))
f = inspect.currentframe()
pprint(dir(f))


def main():
    f0 = inspect.currentframe()
    print('f0: ', f0)
    big_step()


def big_step():
    f1 = inspect.currentframe()
    print('f1', f1)
    small_step()


def small_step():
    print('f2: ', inspect.currentframe())
    return


main()


def run():
    g1 = gen(ident=1)
    g2 = gen(ident=2)

    while 1:
        try:
            next(g1)
        except StopIteration as e:
            print('g1 stopped')
        try:
            next(g2)
        except StopIteration as e:
            print('g2 stopped')
            break


run()


class Iterable(object):
    def __init__(self):
        self.count = 10
        self.curr = 0

    def __iter__(self):
        print('run __iter__')
        return self

    def __next__(self):
        if self.curr < 10:
            self.curr += 1
            return self.curr
        raise StopIteration


x = Iterable()



def cr():
    print('prime ing')
    try:
        x = (yield) + 1

    except GeneratorExit:
        print('co-routine exit')
    else:
        print(f'continue {x}')

c1 = cr()
print('    to prime')
c1.send(None)
print('   primed')
r = c1.send(5)
print('r: ', r)
c1.close()

