import itertools
import random

from django.test import TestCase


# Create your tests here.
class RandomIter:
    def __init__(self, start=1, end=100, max_count=20):
        self.start = start
        self.end = end
        self.max_count = max_count
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count < self.max_count:
            self.count += 1
            return random.randint(1, 100)
        else:
            raise StopIteration()


class FeiBo:
    def __init__(self, max_count=30):
        self.max_count = max_count
        self.count = 0
        self.my_list = []

    def __iter__(self):
        return self

    def iteration(self, n):
        if n == 1:
            return 1
        elif n == 2:
            return 1
        else:
            return self.iteration(n - 1) + self.iteration(n - 2)

    def __next__(self):
        if self.count < self.max_count:
            self.count += 1
            return self.iteration(self.count)
        else:
            raise StopIteration()



if __name__ == '__main__':
    # test1 = RandomIter()
    # for item in test1:
    #     print(item)
    # test2 = FeiBo()
    # for item in test2:
    #     print(item)
    # a = [1, 2]
    # a.insert(1, 4)
    # print(a)


    def ChangeInt(a):
        a = 10
    nfoo = 2
    ChangeInt(nfoo)
    print(nfoo)

    def ChangeInt(a):
        a[0] = 10
    lstFoo = [2]
    ChangeInt(lstFoo)
    print(lstFoo)

    # print([x**2 for x in range(10)])

    # import datetime
    #
    #
    # def getYesterday():
    #     today = datetime.date.today()
    #     oneday = datetime.timedelta(days=1)
    #     yesterday = today - oneday
    #     return yesterday
    #
    #
    # # 输出
    # print(getYesterday())


    def decorator_a(func):
        print('Get in decorator_a')

