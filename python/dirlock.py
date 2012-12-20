import os
import functools

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

        # XXX could do EAFP here to totally eliminate window for racecondition
        if os.path.exists(lock_dir_started):
            if os.path.exists(lock_dir_finished):
                print 'job %s already done. skipping.' % date
            else:
                print 'job %s already started or running. cleanup if you want to restart.' % date
            return

        os.makedirs(lock_dir_started)
        ans = func(date)
        os.makedirs(lock_dir_finished)
        return ans
    return wrapper

@transactional
def test(date):
    print "test done! %s" % str(date)

if __name__ == "__main__":
    from datetime import datetime
    from threading import Thread

    datenow = datetime.now()
    num = 10
    holder = []
    for i in range(num):
        t = Thread(target=test, args=(datenow, ))
        holder.append(t)

    for t in holder:
        t.start()
    for t in holder:
        t.join()

