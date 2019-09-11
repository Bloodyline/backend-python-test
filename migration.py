"""
    Launch the db manager for migrations and db versioning
"""

from resources import manager_db


if __name__ == "__main__":
    manager_db.manager_run()