#! /bin/sh
### BEGIN INIT INFO
# Provides:     redis-server
# Required-Start:   $syslog $remote_fs
# Required-Stop:    $syslog $remote_fs
# Should-Start:     $local_fs
# Should-Stop:      $local_fs
# Default-Start:    2 3 4 5
# Default-Stop:     0 1 6
# Short-Description:    redis-server - Persistent key-value db
# Description:      redis-server - Persistent key-value db
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/local/bin/redis-server
DAEMON_ARGS=/usr/local/etc/redis.conf
NAME=redis-server
DESC=redis-server

RUNDIR=/usr/local/var/run
PIDFILE=$RUNDIR/redis-server.pid

test -x $DAEMON || exit 0

set -e

case "$1" in
  start)
    echo -n "Starting $DESC: "
    mkdir -p $RUNDIR
    touch $PIDFILE
    chmod 755 $RUNDIR
    $DAEMON $DAEMON_ARGS
    ;;
  stop)
    echo -n "Stopping $DESC: "
    cat $PIDFILE | xargs kill -15
    if [ $? -eq 0 ]
    then
        rm -f $PIDFILE
        echo "stopping done"
    else
        echo "stopping failed"
        exit 1
    fi
    ;;

  restart|force-reload)
    ${0} stop
    ${0} start
    ;;

  status)
    echo -n "$DESC is "
    if [ -e $PIDFILE ]
    then
        echo "running"
    else
        echo "not running"
        exit 1
    fi
    ;;

  *)
    echo "Usage: /etc/init.d/$NAME {start|stop|restart|force-reload}" >&2
    exit 1
    ;;
esac

exit 0
