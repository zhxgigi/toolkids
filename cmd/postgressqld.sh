cmd=$1
pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log $cmd
#pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log restart
