import pytest
from main import app
from application.models import db, Role

@pytest.fixture(autouse=True)
def bypass_auth(monkeypatch):
    def fake_decorator(*args, **kwargs):
        def wrapper(fn):
            return fn
        return wrapper

    # patch everywhere
    monkeypatch.setattr("application.views.auth_required", fake_decorator, raising=False)
    monkeypatch.setattr("application.views.roles_required", fake_decorator, raising=False)

    monkeypatch.setattr("application.resources.auth_required", fake_decorator, raising=False)
    monkeypatch.setattr("application.resources.roles_required", fake_decorator, raising=False)

    monkeypatch.setattr("flask_security.decorators.auth_required", fake_decorator, raising=False)
    monkeypatch.setattr("flask_security.decorators.roles_required", fake_decorator, raising=False)

@pytest.fixture
def app_fixture():
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app_fixture):
    with app_fixture.app_context():
        db.create_all()

        roles = ["owner", "manager", "staff", "customer"]
        for r in roles:
            if not Role.query.filter_by(name=r).first():
                db.session.add(Role(name=r))

        db.session.commit()

        yield app_fixture.test_client()

        db.session.remove()
        db.drop_all()