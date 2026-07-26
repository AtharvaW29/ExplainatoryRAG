from httpx import AsyncClient


async def test_concept_crud_lifecycle(client: AsyncClient) -> None:
    created = await client.post(
        "/concept",
        json={
            "name": "Gradient Descent",
            "description": "Optimization using a loss gradient.",
            "difficulty": "intermediate",
            "domain": "Machine Learning",
        },
    )

    assert created.status_code == 201, created.text
    concept_id = created.json()["id"]

    fetched = await client.get(f"/concept/{concept_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Gradient Descent"

    patched = await client.patch(
        f"/concept/{concept_id}",
        json={
            "description": "Iterative first-order optimization.",
            "difficulty": "advanced",
        },
    )
    assert patched.status_code == 201
    assert patched.json()["difficulty"] == "advanced"

    listed = await client.get("/concept")
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [concept_id]

    deleted = await client.delete(
        f"/concept/{concept_id}",
        params={"isdeleted": "true"},
    )
    assert deleted.status_code == 204

    listed_after_delete = await client.get("/concept")
    assert listed_after_delete.status_code == 200
    assert listed_after_delete.json() == []

    inactive_by_name = await client.get("/concept/name/Gradient%20Descent")
    assert inactive_by_name.status_code == 404
