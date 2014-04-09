#! /bin/bash
#
# startmongod.sh
# (C) 2013 hongxun <hongxun@hongxuns-mac.local>
#

if [[ $# != 1 ]]; then
    echo "Usage: $0 Tasktype"
    echo "Tasktype: estimate, curve_sync, weekly_regen"
    exit 2
fi

NAME="mongod"
DESC="mongod"
PIDFILE="/usr/local/Cellar/mongodb/2.4.8/mongod.pid"

case "$1" in
  start)
    echo -n "Starting $DESC: "
    mongod -f /usr/local/Cellar/mongodb/2.4.8/mongodb.conf --pidfilepath=$PIDFILE
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
