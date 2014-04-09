#! /bin/bash
#
# supervisexun.sh
# Copyright (C) 2013 hongxun <hongxun@hongxuns-mac.local>
#
# Distributed under terms of the MIT license.

workon xun
supervisord -c $HOME/projects/toolkids/supervised/supervisord.conf
supervisorctl -c $HOME/projects/toolkids/supervised/supervisord.conf restart all
