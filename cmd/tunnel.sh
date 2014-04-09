#! /bin/bash
#
# supervisexun.sh
# Copyright (C) 2013 hongxun <hongxun@hongxuns-mac.local>
#
# Distributed under terms of the MIT license.
#


/Users/hongxun/.virtualenvs/aa/bin/supervisord -c /Users/hongxun/Dropbox/share/projects/toolkids/supervised/supervisord.conf

/Users/hongxun/.virtualenvs/aa/bin/supervisorctl -c /Users/hongxun/Dropbox/share/projects/toolkids/supervised/supervisord.conf restart all
