import click
from todo.users.models import Role, User
from flask.cli import AppGroup


def cli_register(app):

    init_cli = AppGroup('init')

    @init_cli.command('database')
    def init_db():
        for role in app.config['SYSTEM_ROLES']:
            role = Role(title=role).save()
            click.echo(f'Role {role} added')

    app.cli.add_command(init_cli)

    @init_cli.command('administrator')
    @click.option("--email", prompt="Administrator's email address", help="Administrator's email address")
    @click.option("--first_name", prompt="Administrator's first name", help="Administrator's first name")
    @click.option("--last_name", prompt="Administrator's last name", help="Administrator's last name")
    @click.option("-p", "--password", prompt="Enter password", hide_input=True, confirmation_prompt=True,
                  help="Password for administrator")
    def create_administrator(email, first_name, last_name, password):
        user = Role.objects(title='user').get()
        administrator = Role.objects(title='administrator').get()
        admin = User(email=email, first_name=first_name, last_name=last_name, roles=[user, administrator])
        admin.password = User.generate_password(password)
        admin.save()
        click.echo(f'Administrator {first_name} {last_name} {email} created')
