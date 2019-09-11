"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
import alayatodo
from alayatodo import app
from docopt import docopt
import subprocess
import os, errno

def _run_sql(filename):
    try:
        # Check if the db file exist, if not create it
        if not os.path.exists(app.config['DATABASE']):
            # Check if the directory exist
            if not os.path.exists(os.path.dirname(app.config['DATABASE'])):
                try:
                    # Make the directory if not found
                    os.makedirs(os.path.dirname(app.config['DATABASE']))
                # Guard against race condition
                except OSError as exc: 
                    if exc.errno != errno.EEXIST:
                        raise

            # Create the db file
            open(app.config['DATABASE'], "w+").close()

        subprocess.check_output(
            f"sqlite3 {app.config['DATABASE']} < {filename}",
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError as ex:
        print(ex.output)
        os._exit(1)


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        # _run_sql('resources/database.sql')
        _run_sql('resources/fixtures.sql')
        print("AlayaTodo: Database initialized.")
    else:
        app.run(use_reloader=True)
