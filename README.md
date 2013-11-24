wdtest
======
    $ cd <directory containing this file>
    $ mkvirtualenv wdtest
    $ pip install -r requirements.txt
    $ wget https://www.dropbox.com/s/ye9kmm7tmlmuosn/img.tar.gz
    $ tar -xzf img.tar.gz
    $ python manage.py syncdb
    $ python manage.py runserver
