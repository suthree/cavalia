+import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server, Shell
from flask_script.commands import Clean, ShowUrls

from blink.app import create_app
from blink.database import db
from blink.settings import DevConfig, ProdConfig
from blink.user.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(BASE_DIR, 'tests')

manager = Manager(app)
migrate = Migrate(app, db)


def _make_shell_context():
    return dict(app=app, db=db, user=User)


@manager.command
def test():
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code

manager.add_command('server', Server())
manager.add_command("shell", Shell(make_context=_make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('urls', ShowUrls())
manager.add_command('clean', Clean())



if __name__ == '__main__':
    manager.run()

