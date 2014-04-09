#! /bin/bash
#
# install.sh
# (C) 2014 hongxun <hongxun@hongxuns-mac.lan.appannie.com>
#

set -e
set -u
set -o pipefail


currentdir=`pwd`
echo $currentdir
if [ -d ~/cmd ]; then
    mv ~/cmd ~/cmd_bak
fi

ln -s $currentdir/cmd ~/cmd
