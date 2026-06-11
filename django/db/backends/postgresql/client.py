import os
import signal
import subprocess

from django.db.backends.base.client import BaseDatabaseClient

    def runshell_db(cls, conn_params):
        args = [cls.executable_name]

        host = conn_params.get('host', '')
        port = conn_params.get('port', '')
        dbname = conn_params.get('database', '')
        user = conn_params.get('user', '')
        passwd = conn_params.get('password', '')

        port = conn_params.get('port', '')
        if port:
            args += ['-p', str(port)]
        args += [dbname]

        subprocess_env = os.environ.copy()
        if passwd:
            subprocess_env['PGPASSWORD'] = passwd

        sigint_handler = signal.getsignal(signal.SIGINT)

            # Allow SIGINT to pass to psql to abort queries.
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            subprocess.run(args, env=subprocess_env, check=True)
        finally:
            # Restore the original SIGINT handler.
            signal.signal(signal.SIGINT, sigint_handler)
            # if temp_pgpass:
                pass # No need to close temp file, it is not used

    def runshell(self):
        DatabaseClient.runshell_db(self.connection.get_connection_params())




                temp_pgpass.close()
                if 'PGPASSFILE' in os.environ:  # unit tests need cleanup
                    del os.environ['PGPASSFILE']

    def runshell(self):
        DatabaseClient.runshell_db(self.connection.get_connection_params())
