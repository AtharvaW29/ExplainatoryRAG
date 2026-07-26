from httpx import AsyncClient

from .conftest import UserFactory


async def test_user_routes_reject_cross_user_access(
    client: AsyncClient,
    user_factory: UserFactory,
) -> None:
    alice = await user_factory("Alice", "alice@example.com")
    bob = await user_factory("Bob", "bob@example.com")

    read_bob = await client.get(
        "/users/bob@example.com",
        headers=alice["headers"],
    )
    patch_bob = await client.patch(
        f"/users/{bob['user']['id']}",
        headers=alice["headers"],
        json={"name": "Compromised Bob"},
    )

    assert read_bob.status_code == 403
    assert patch_bob.status_code == 403

    read_self = await client.get(
        "/users/alice@example.com",
        headers=alice["headers"],
    )
    assert read_self.status_code == 200


async def test_learner_profile_is_owner_only(
    client: AsyncClient,
    user_factory: UserFactory,
) -> None:
    alice = await user_factory("Alice", "alice@example.com")
    bob = await user_factory("Bob", "bob@example.com")
    alice_id = alice["user"]["id"]
    bob_id = bob["user"]["id"]

    created = await client.post(
        "/learner_profile",
        headers=alice["headers"],
        json={
            "user_id": alice_id,
            "academic_level": "graduate",
            "learning_style": "visual",
            "domain": ["Machine Learning"],
            "language": "English",
        },
    )
    assert created.status_code == 201, created.text

    own_profile = await client.get(
        f"/learner_profile/{alice_id}",
        headers=alice["headers"],
    )
    cross_read = await client.get(
        f"/learner_profile/{alice_id}",
        headers=bob["headers"],
    )
    cross_patch = await client.patch(
        f"/learner_profile/{bob_id}",
        headers=alice["headers"],
        json={"academic_level": "changed"},
    )

    assert own_profile.status_code == 200
    assert cross_read.status_code == 403
    assert cross_patch.status_code == 403


async def test_mastery_uses_authenticated_user_identity(
    client: AsyncClient,
    user_factory: UserFactory,
) -> None:
    alice = await user_factory("Alice", "alice@example.com")
    bob = await user_factory("Bob", "bob@example.com")

    concept = await client.post(
        "/concept",
        json={"name": "Backpropagation"},
    )
    assert concept.status_code == 201
    concept_id = concept.json()["id"]

    cross_user_write = await client.post(
        "/mastery",
        headers=alice["headers"],
        json={
            "user_id": bob["user"]["id"],
            "concept_id": concept_id,
            "mastery_score": 0.8,
            "confidence": 0.7,
        },
    )
    assert cross_user_write.status_code == 403

    own_write = await client.post(
        "/mastery",
        headers=alice["headers"],
        json={
            "user_id": alice["user"]["id"],
            "concept_id": concept_id,
            "mastery_score": 0.8,
            "confidence": 0.7,
        },
    )
    assert own_write.status_code == 201, own_write.text

    own_read = await client.get(
        f"/mastery/{concept_id}",
        headers=alice["headers"],
    )
    bob_read = await client.get(
        f"/mastery/{concept_id}",
        headers=bob["headers"],
    )
    anonymous_read = await client.get(f"/mastery/{concept_id}")

    assert own_read.status_code == 200
    assert bob_read.status_code == 404
    assert anonymous_read.status_code == 401


async def test_explanation_session_cannot_be_read_by_another_user(
    client: AsyncClient,
    user_factory: UserFactory,
) -> None:
    alice = await user_factory("Alice", "alice@example.com")
    bob = await user_factory("Bob", "bob@example.com")

    created = await client.post(
        "/explanation_sessions",
        headers=alice["headers"],
        json={
            "user_id": bob["user"]["id"],
            "topic": "Backpropagation",
            "explanations": [
                {
                    "prompt": "Explain backpropagation.",
                    "generated_explanation": "A test explanation.",
                    "difficulty_score": 5,
                    "explanation_style": "concise",
                    "token_count": 12,
                    "llm_provider": "test",
                    "llm_model": "test-model",
                    "generation_time_ms": 1.0,
                }
            ],
        },
    )
    assert created.status_code == 201, created.text

    history = await client.get(
        "/explanation_sessions",
        headers=alice["headers"],
    )
    assert history.status_code == 200
    session_id = history.json()["sessions"][0]["id"]

    own_read = await client.get(
        f"/explanation_sessions/{session_id}",
        headers=alice["headers"],
    )
    cross_user_read = await client.get(
        f"/explanation_sessions/{session_id}",
        headers=bob["headers"],
    )

    assert own_read.status_code == 200
    assert own_read.json()["user_id"] == alice["user"]["id"]
    assert cross_user_read.status_code == 404

    explanation_id = own_read.json()["explanations"][0]["id"]
    feedback = await client.post(
        "/feedback",
        headers=alice["headers"],
        json={
            "explanation_id": explanation_id,
            "rating": 5,
            "clarity_score": 5,
            "usefulness_score": 4,
            "correctness_score": 5,
            "comments": "Clear explanation.",
        },
    )
    assert feedback.status_code == 201

    own_feedback = await client.get(
        f"/feedback/{explanation_id}",
        headers=alice["headers"],
    )
    cross_user_feedback = await client.get(
        f"/feedback/{explanation_id}",
        headers=bob["headers"],
    )
    anonymous_feedback = await client.get(
        f"/feedback/{explanation_id}",
    )

    assert own_feedback.status_code == 200
    assert cross_user_feedback.status_code == 404
    assert anonymous_feedback.status_code == 401
