from todo import create_app
import os

# Getting WORK_ENV variable and create Flask object.
env = os.environ.get('WORK_ENV', 'Dev')
app = create_app(f'config.{env.capitalize()}Config')

if __name__ == '__main__':
    app.run()
