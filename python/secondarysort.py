data = [
        ("a",100),("b",100),("c",100),
        ("d", 98), ("e",98),("f", 98),
        ("f", 97), ("g", 96)
        ]

import random
random.shuffle(data)
print data

data.sort(key=lambda item: (item[1], item[0]), reverse=True)
print data


def mycmp(item1, item2):
    if item1[1] != item2[1]:
        return cmp(item1[1], item2[1])
    else:
        return 0 - cmp(item1[0], item2[0])

random.shuffle(data)
data.sort(cmp=mycmp, reverse=True)
print data
from operator import itemgetter

def secondary_sort(data):
    return sorted(sorted(data, key=itemgetter(0)),
                key=itemgetter(1), reverse=True)
data = [
                (1, 10.0), (2, 11.0), (3, 12.0),
                (4, 10.0), (5, 14.0), (4, 15.0),
                (0, 15.0),
        ]
result = [(0, 15.0), (4, 15.0), (5, 14.0), (3, 12.0), (2, 11.0), (1, 10.0), (4, 10.0)]

