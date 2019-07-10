# coding:utf8
import sys
import time,gevent
from multiprocessing import Process
import asyncio


def work(*args):
    # assert len(args) == 3
    m, c, f = args[0]
    print(m, c, f)
    try:
        m = __import__(m, fromlist=True)
    except TypeError:
        print("未发现名为{}的库".format(m))
        sys.exit(1)
    if hasattr(m, c):
        c = getattr(m, c)
    else:
        print("该库为包含{}类".format(c))
        sys.exit(1)
    if hasattr(c, f):
        f = getattr(c(), f)
        f()
    else:
        print("该类未实现{}方法".format(f))
        sys.exit(1)


@asyncio.coroutine
def work2(*args):
    # assert len(args) == 3
    m, c, f = args[0]
    print(m, c, f)
    try:
        m = __import__(m, fromlist=True)
    except TypeError:
        print("未发现名为{}的库".format(m))
        sys.exit(1)
    if hasattr(m, c):
        c = getattr(m, c)
    else:
        print("该库为包含{}类".format(c))
        sys.exit(1)
    if hasattr(c, f):
        f = getattr(c(), f)
        f()
    else:
        print("该类未实现{}方法".format(f))
        sys.exit(1)


if __name__ == "__main__":
    '''
    t1 = time.time()
    gevent.joinall([
        gevent.spawn(work, ("jobs.gjtjj", 'GjtjjClass', 'run',)),
        gevent.spawn(work, ("jobs.gjtjj", 'GjtjjClass', 'say',))
    ])
    t2 = time.time()
    '''
    t3 = time.time()
    work(("jobs.zqgz", 'ZqgzClass', 'run',))
    t4 = time.time()
    '''
    print("多进程实现")
    t5 = time.time()
    ps = []
    for i, k in enumerate([[("jobs.gjtjj", 'GjtjjClass', 'say',)], [("jobs.gjtjj", 'GjtjjClass', 'run',)]]):
        p = Process(target=work, name="work"+str(i),args= k)
        ps.append(p)
    for p in ps:
        p.start()
    for p in ps:
        p.join()
    t6 = time.time()
    print("异步实现")
    t7 = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(map(work2, [("jobs.gjtjj", 'GjtjjClass', 'say',), ("jobs.gjtjj", 'GjtjjClass', 'run',)])))
    loop.close()
    t8 = time.time()

    print("twisted 异步")

    print("{}-{}-{}-{}".format(t2-t1, t4-t3, t6-t5, t8-t7))
    print("Ending...")'''
