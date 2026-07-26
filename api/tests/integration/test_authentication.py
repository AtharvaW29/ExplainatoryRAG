from httpx import AsyncClient

from src.core.security import create_access_token

from .conftest import UserFactory


async def test_register_login_and_get_current_user(
    client: AsyncClient,
) -> None:
    registration = await client.post(
        "/auth/register",
        json={
            "name": "Alice",
            "email": "alice@example.com",
            "password": "Password123!",
        },
    )

    assert registration.status_code == 201
    assert registration.json()["email"] == "alice@example.com"
    assert "password" not in registration.json()
    assert "password_hash" not in registration.json()

    login = await client.post(
        "/auth/login",
        json={
            "email": "alice@example.com",
            "password": "Password123!",
        },
    )

    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"

    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {login.json()['access_token']}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == registration.json()["id"]


async def test_duplicate_registration_is_rejected(
    client: AsyncClient,
    user_factory: UserFactory,
) -> None:
    await user_factory("Alice", "alice@example.com")

    response = await client.post(
        "/auth/register",
        json={
            "name": "Another Alice",
            "email": "alice@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


async def test_bad_password_is_rejected(
    client: AsyncClient,
    user_factory: UserFactory,
) -> None:
    await user_factory("Alice", "alice@example.com")

    response = await client.post(
        "/auth/login",
        json={
            "email": "alice@example.com",
            "password": "DefinitelyWrong",
        },
    )

    assert response.status_code == 401


async def test_missing_invalid_and_expired_tokens_are_rejected(
    client: AsyncClient,
    user_factory: UserFactory,
) -> None:
    created = await user_factory("Alice", "alice@example.com")

    missing = await client.get("/auth/me")
    invalid = await client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )
    expired_token = create_access_token(
        subject=created["user"]["id"],
        expires_minutes=-1,
    )
    expired = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )

    assert missing.status_code == 401
    assert invalid.status_code == 401
    assert expired.status_code == 401
