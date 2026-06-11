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

    @classmethod
    def runshell_db(cls, conn_params):
        ssl_options = conn_params.get('OPTIONS', {})
        args = [cls.executable_name]

        if ssl_options.get('sslcert'):
            args.append('-sslcert')
            args.append(ssl_options['sslcert'])
        if ssl_options.get('sslkey'):
            args.append('-sslkey')
            args.append(ssl_options['sslkey'])
        if ssl_options.get('sslrootcert'):
            args.append('-sslrootcert')
            args.append(ssl_options['sslrootcert'])
        host = conn_params.get('host', '')
        port = conn_params.get('port', '')
        dbname = conn_params.get('database', '')
        subprocess_env = os.environ.copy()
        if passwd:
            subprocess_env['PGPASSWORD'] = str(passwd)
        try:
            # Allow SIGINT to pass to psql to abort queries.
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            subprocess.run(args, check=True, env=subprocess_env)
        finally:
            args += ['-p', str(port)]
        args += [dbname]

        if user:
            args += ['-U', user]
        if host:
            args += ['-h', host]
            subprocess_env['PGPASSWORD'] = str(passwd)
        try:
            # Allow SIGINT to pass to psql to abort queries.
            subprocess.run(args, check=True, env=subprocess_env)
        finally:
            # Restore the original SIGINT handler.
    def runshell(self):
        DatabaseClient.runshell_db(self.connection.get_connection_params())
```