from todo import create_app
from todo.cli import cli_register
import os

# Getting WORK_ENV variable and create Flask object.
env = os.environ.get('WORK_ENV', 'Dev')
app = create_app(f'config.{env.capitalize()}Config')
cli_register(app)

if __name__ == '__main__':
    app.run()
