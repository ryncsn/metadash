A webservice to manage testrun, testcase, statistic and metadata, powered by Flask.

WIP

For a faster start up, you need pipenv

Install Requirements For PY:

    pipenv install

Install Requirements For JS:

    npm install

Build bundle files:

    ./node_modules/webpack/bin/webpack.js

Run Server:

    ./manager.py runserver

Test Server:

    ./manager.py testserver

Generate some fixtures:

    ./manager.py genfixture

Upgrade db from older version:

    ./manager.py db upgrade

Integrate With apache-wsgi:

    Retrive a wsgi file

        ./manager.py wsgi > wsgi.py

    Selinux config:

        setsebool -P httpd_can_network_connect 1
        chcon /path/to/metadash/instance -t httpd_sys_content_t -R

    Create virtual host file:
        <VirtualHost example.domain.com:80>
            WSGIDaemonProcess metadash user=nobody group=nobody threads=5 python-path=/var/www/metadash
            WSGIScriptAlias / /var/www/metadash/wsgi.py

            <Directory /var/www/metadash>
                WSGIProcessGroup metadash
                WSGIApplicationGroup %{GLOBAL}
                Require all granted
            </Directory>
        </VirtualHost>
