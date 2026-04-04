import pytest
from main import app
from application.models import db, Role

@pytest.fixture(autouse=True)
def bypass_auth(monkeypatch,request):
    if "no_auth_bypass" in request.node.keywords:
        return
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
    app.config["SECURITY_REDIRECT_BEHAVIOR"] = "spa"
    app.config["SECURITY_UNAUTHORIZED_VIEW"] = None
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

from application.models import User
from flask_security.utils import hash_password

@pytest.fixture
def create_user():
    def _create_user(username, password, role_name):
        role = Role.query.filter_by(name=role_name).first()
        assert role is not None, f"Role '{role_name}' not found in DB"
        user = User(
            username=username,
            password=hash_password(password),
            roles=[role]
        )

        db.session.add(user)
        db.session.commit()
        return user

    return _create_user

@pytest.fixture
def get_token(client, create_user):
    def _get_token(username, password, role):
        create_user(username, password, role)

        res = client.post(f"/{role}-login", json={
            "username": username,
            "password": password
        })

        return res.get_json()["token"]

    return _get_token

