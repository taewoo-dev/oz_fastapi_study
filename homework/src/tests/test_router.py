from core.authenticate.services.authenticate_service import AuthenticateService
from users.domains.user import User


def test_root(client):
    # given

    # when
    response = client.get("/")

    # then
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_sign_up(client, test_session):
    # given

    # when
    response = client.post(
        "/users/sign-up",
        json={
            "username": "test_user",
            "password": "test_password",
        },
    )

    # then
    assert response.status_code == 201
    assert type(response.json()["id"]) == int
    assert response.json()["username"] == "test_user"
    assert response.json()["created_at"]

    user = test_session.query(User).filter(User.username == "test_user").first()
    assert user
    assert AuthenticateService.check_password(
        input_password="test_password",
        hashed_password=user.password,
    )


def test_sign_in(client, test_session):
    # given
    new_user = User.create(
        username="test_user",
        password=AuthenticateService.hash_password("test_password"),
    )
    test_session.add(new_user)
    test_session.commit()

    # when
    response = client.post(
        "/users/sign-in",
        json={
            "username": "test_user",
            "password": "test_password",
        },
    )

    access_token = response.json()["access_token"]
    refresh_token = response.json()["refresh_token"]

    # then
    assert response.status_code == 200
    assert access_token
    assert refresh_token


def test_get_me(client, test_session):
    # given
    new_user = User.create(
        username="test_user",
        password=AuthenticateService.hash_password("test_password"),
    )
    test_session.add(new_user)
    test_session.commit()

    access_token = AuthenticateService.create_access_token(new_user.username)

    # when
    response = client.post(
        "/users/me/", headers={"Authorization": f"Bearer {access_token}"}
    )
