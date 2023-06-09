import nox


@nox.session
def lint(session):
    session.install("black")
    session.install("isort")
    session.run("isort", ".")
    session.run("black", ".")


@nox.session
def unit_test(session):
    session.install("-r", "requirements.txt")
    session.run("coverage", "run", "-m", "pytest")


@nox.session
def e2e_test(session):
    session.install("-r", "requirements.txt")
    session.run("coverage", "run", "-m", "pytest", "-v", "./tests/e2e")
