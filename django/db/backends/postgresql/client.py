import os
import subprocess

from django.core.files.utils import abspath_for_command

from django.db.backends.base.client import BaseDatabaseClient


def _escape_pgpass(txt):
    """
        return 'psql'

    def runshell(self):
        dbname = self.connection.get_database_name()
        settings_dict = self.connection.settings_dict

        args = [self.executable]
        options = settings_dict.get('OPTIONS', {})
        host = settings_dict.get('HOST')
        port = settings_dict.get('PORT')
        user = settings_dict.get('USER')
        passwd = settings_dict.get('PASSWORD')

        if user:
            args += ['-U', user]
        if host:
            args += ['-h', host]
        if port:
            args += ['-p', str(port)]

        args += [dbname]

        env = os.environ.copy()
        if passwd:
            env['PGPASSWORD'] = passwd

        try:
            subprocess.run(args, env=env)
        except Exception as e:
            raise e
                        _escape_pgpass(host) or '*',
                        str(port) or '*',
                        _escape_pgpass(dbname) or '*',
                        _escape_pgpass(user) or '*',
                        _escape_pgpass(passwd),
                        file=temp_pgpass,
                        sep=':',
                        flush=True,
                    )
                    os.environ['PGPASSFILE'] = temp_pgpass.name
                except UnicodeEncodeError:
                    # If the current locale can't encode the data, let the
                    # user input the password manually.
                    pass
            # Allow SIGINT to pass to psql to abort queries.
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            subprocess.check_call(args)
        finally:
            # Restore the original SIGINT handler.
            signal.signal(signal.SIGINT, sigint_handler)
            if temp_pgpass:
                temp_pgpass.close()
                if 'PGPASSFILE' in os.environ:  # unit tests need cleanup
                    del os.environ['PGPASSFILE']

    def runshell(self):
        DatabaseClient.runshell_db(self.connection.get_connection_params())
