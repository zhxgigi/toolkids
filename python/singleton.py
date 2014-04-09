
class Singleton(object):
    def __new__(cls, *args, **argkw):
        if not hasattr(cls, "_instance"):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **argkw)
        return cls._instance


class MyClass(Singleton):
    def __init__(self):
        self.name = "zhang"


for i in range(10):
    ss = MyClass()
    print id(ss)


class MySubClass(MyClass):
    age = 10

msc = MySubClass()
