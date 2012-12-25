import os
import functools
import time

def transactional(func):
    lock_root = os.path.join('locks', func.__name__)
    try:
        os.makedirs(lock_root)
    except:
        pass

    @functools.wraps(func)
    def wrapper(date):
        lock_dir_started = os.path.join(lock_root, '%s-started' % date.strftime('%Y-%m-%d'))
        lock_dir_finished = os.path.join(lock_root, '%s-finished' % date.strftime('%Y-%m-%d'))

        try:
            os.makedirs(lock_dir_started)
            ans = func(date)
            os.makedirs(lock_dir_finished)
            return ans
        except OSError:
            try:
                os.makedirs(lock_dir_finished)
                print "job %s alreday done. skipping." % date
            except OSError:
                print 'job %s already started or running. cleanup if you want to restart.' % date
    return wrapper


@transactional
def test(date):
    time.sleep(4)
    print "test done! %s" % str(date)

if __name__ == "__main__":
    from datetime import datetime
    from threading import Thread
    from datetime import timedelta
    import random

    daterange = []
    startdate = datetime.now()
    enddate = startdate + timedelta(days=5)
    while startdate <= enddate:
        daterange.append(startdate)
        startdate += timedelta(days=1)
    num = 20
    holder = []
    for i in range(num):
        t = Thread(target=test, args=(daterange[random.randint(0, len(daterange)-1)], ))
        holder.append(t)

    for t in holder:
        t.start()
    for t in holder:
        t.join()

