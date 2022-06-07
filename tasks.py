import subprocess

from invoke import task


@task
def clean(ctx):
    print('Running clean...')
    ctx.run('find . -name "*.pyc" -exec rm {} +')


@task(clean)
def test_unit(ctx):
    """
    Run any unit tests
    """
    print('Running unit tests...')

    cmd = 'python -m unittest discover -s tests -p "*_unit_test.py" -v'
    subprocess.check_call(cmd,  shell=True)


@task
def lint(ctx):
    """
    Run lint checks
    """
    print('Running linting...')
    ctx.run('flake8')


@task(lint, test_unit)
def ci(ctx):
    """
    Run all the applicable tests that our CI process runs.
    """
    print('Running CI...')
