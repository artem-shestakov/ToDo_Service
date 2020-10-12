from todo import create_app, init_celery, celery
from todo.cli import cli_register
import os
from flask_swagger_ui import get_swaggerui_blueprint

# Getting WORK_ENV variable and create Flask object.
env = os.environ.get('WORK_ENV', 'Dev')
app = create_app(f'config.{env.capitalize()}Config')

# Register CLI commands
cli_register(app)

# Init Celery object
init_celery(app, celery=celery)

if __name__ == '__main__':
    app.run()
