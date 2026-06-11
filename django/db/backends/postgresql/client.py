import os
import signal
import subprocess

from django.db.backends.base.client import BaseDatabaseClient


class DatabaseClient(BaseDatabaseClient):
    executable_name = 'psql'

    @classmethod
    def runshell_db(cls, conn_params):
        args = [cls.executable_name]

        host = conn_params.get('host', '')
        port = conn_params.get('port', '')
        dbname = conn_params.get('database', '')
        user = conn_params.get('user', '')
        passwd = conn_params.get('password', '')

        if user:
            args += ['-U', user]
        if host:
            args += ['-h', host]
        if port:
            args += ['-p', str(port)]
        args += [dbname]

        sigint_handler = signal.getsignal(signal.SIGINT)
        subprocess_env = os.environ.copy()
        if passwd:
            subprocess_env['PGPASSWORD'] = str(passwd)
        try:
            # Allow SIGINT to pass to psql to abort queries.
                    args += ['-U', settings_dict['USER']]
                if settings_dict.get('PASSWORD'):
                    args += ['-w']

                # Add SSL certificate parameters if present
                ssl_options = settings_dict.get('OPTIONS', {})
                if ssl_options.get('sslmode'):
                    args += ['-sslmode', ssl_options['sslmode']]
                if ssl_options.get('sslcert'):
                    args += ['-sslcert', ssl_options['sslcert']]
                if ssl_options.get('sslkey'):
                    args += ['-sslkey', ssl_options['sslkey']]
                if ssl_options.get('sslrootcert'):
                    args += ['-sslrootcert', ssl_options['sslrootcert']]

                if settings_dict.get('PORT'):
                    args += ['-p', settings_dict['PORT']]
