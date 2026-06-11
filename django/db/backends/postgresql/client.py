import os
import signal
import subprocess

from django.core.files.temp import NamedTemporaryFile
from django.db.backends.base.client import BaseDatabaseClient


def _escape_pgpass(txt):
    """
    Escape a fragment of a PostgreSQL .pgpass file.
    """
from django.core.files.temp import NamedTemporaryFile
from django.db.backends.base.client import BaseDatabaseClient

import os
import subprocess

def _escape_pgpass(txt):
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

        temp_pgpass = None
        sigint_handler = signal.getsignal(signal.SIGINT)
        try:
            if passwd:
                # Create temporary .pgpass file.
                temp_pgpass = NamedTemporaryFile(mode='w+')
                try:
                    print(
        password = settings_dict.get('PASSWORD')
        db_name = settings_dict.get('NAME')
        defaults = {'host': host, 'port': port, 'database': db_name}
        
        env = os.environ.copy()
        try:
            args += cls.settings_to_cmd_args_env(settings_dict, parameters)
            if password:
                env['PGPASSWORD'] = password
            subprocess.run(args, env=env, check=True)
        except subprocess.CalledProcessError:
            pass

    def runshell(self):
        DatabaseClient.runshell_db(self.connection.get_connection_params())
        DatabaseClient.runshell_db(self.connection.get_connection_params())
