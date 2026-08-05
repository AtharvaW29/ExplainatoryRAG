from fastapi.testclient import TestClient
from starlette.testclient import WebSocketTestSession

from src.main import app


def test_ping_and_mock_gen(
    chat_websocket: WebSocketTestSession,  # type: ignore
) -> None:
    with TestClient(app) as client:
        with client.websocket_connect(
            "/explanation_sessions/start_exp_session",
            subprotocols=["llm-chat.v1"],
        ) as websocket:
            websocket.send_json(
                {
                    "v": 1,
                    "type": "ping",
                    "request_id": ("10000000-0000-4000-8000-000000000001"),
                    "payload": {
                        "nonce": "pytest-ping",
                    },
                }
            )

            # pong = websocket.receive_json()
            pong = chat_websocket.receive_json()

            assert pong["type"] == "pong"
            assert pong["payload"]["nonce"] == "pytest-ping"

            websocket.send_json(
                {
                    "v": 1,
                    "type": "chat.send",
                    "request_id": ("20000000-0000-4000-8000-000000000002"),
                    "payload": {
                        "conversation_id": None,
                        "content": "Test message",
                    },
                }
            )

            received_types: list[str] = []
            sequence_numbers: list[int] = []

            while True:
                # event = websocket.receive_json()
                event = chat_websocket.receive_json()
                received_types.append(event["type"])
                sequence_numbers.append(event["seq"])

                if event["type"] == "generation.completed":
                    break

            assert received_types[0] == "chat.accepted"
            assert received_types[1] == "generation.started"
            assert "generation.delta" in received_types
            assert received_types[-1] == "generation.completed"

            assert sequence_numbers == list(range(len(sequence_numbers)))


def test_ping_returns_pong(
    chat_websocket: WebSocketTestSession,
) -> None:
    request_id = "10000000-0000-4000-8000-000000000001"

    chat_websocket.send_json(
        {
            "v": 1,
            "type": "ping",
            "request_id": request_id,
            "payload": {
                "nonce": "pytest-ping",
            },
        }
    )

    event = chat_websocket.receive_json()

    assert event["v"] == 1
    assert event["type"] == "pong"
    assert event["request_id"] == request_id
    assert event["seq"] == 0
    assert event["payload"]["nonce"] == "pytest-ping"


def test_chat_streams_mock_generation(
    chat_websocket: WebSocketTestSession,
) -> None:
    request_id = "20000000-0000-4000-8000-000000000002"

    chat_websocket.send_json(
        {
            "v": 1,
            "type": "chat.send",
            "request_id": request_id,
            "payload": {
                "conversation_id": None,
                "content": "Test message",
            },
        }
    )

    events: list[dict] = []

    while True:
        event = chat_websocket.receive_json()
        events.append(event)

        if event["type"] == "generation.completed":
            break

    event_types = [event["type"] for event in events]
    sequence_numbers = [event["seq"] for event in events]

    assert event_types[0] == "chat.accepted"
    assert event_types[1] == "generation.started"
    assert "generation.delta" in event_types
    assert event_types[-1] == "generation.completed"

    assert sequence_numbers == list(range(len(events)))

    assert all(event["request_id"] == request_id for event in events)

    conversation_ids = {event["conversation_id"] for event in events}

    assert len(conversation_ids) == 1

    streamed_text = "".join(
        event["payload"]["text"]
        for event in events
        if event["type"] == "generation.delta"
    )

    assert streamed_text
    assert "Test message" in streamed_text


def test_invalid_chat_event_returns_error(
    chat_websocket: WebSocketTestSession,
) -> None:
    chat_websocket.send_json(
        {
            "v": 1,
            "type": "chat.send",
            "request_id": ("30000000-0000-4000-8000-000000000003"),
            "payload": {
                "content": "",
                "unexpected_field": True,
            },
        }
    )

    event = chat_websocket.receive_json()

    assert event["type"] == "error"
    assert event["payload"]["code"] == "invalid_event"
    assert event["payload"]["retryable"] is False


def test_unknown_event_type_returns_error(
    chat_websocket: WebSocketTestSession,
) -> None:
    chat_websocket.send_json(
        {
            "v": 1,
            "type": "unsupported.event",
            "request_id": ("40000000-0000-4000-8000-000000000004"),
            "payload": {},
        }
    )

    event = chat_websocket.receive_json()

    assert event["type"] == "error"
    assert event["payload"]["code"] == "invalid_event"


def test_active_generation_can_be_cancelled(
    chat_websocket: WebSocketTestSession,
) -> None:
    generation_request_id = "50000000-0000-4000-8000-000000000005"

    chat_websocket.send_json(
        {
            "v": 1,
            "type": "chat.send",
            "request_id": generation_request_id,
            "payload": {
                "conversation_id": None,
                "content": "Generate a response to cancel",
            },
        }
    )

    # Wait until generation has started.
    while True:
        event = chat_websocket.receive_json()

        if event["type"] == "generation.started":
            break

    chat_websocket.send_json(
        {
            "v": 1,
            "type": "generation.cancel",
            "request_id": ("60000000-0000-4000-8000-000000000006"),
            "payload": {
                "generation_request_id": generation_request_id,
            },
        }
    )

    while True:
        event = chat_websocket.receive_json()

        if event["type"] in {
            "generation.cancelled",
            "generation.completed",
        }:
            break

    assert event["type"] == "generation.cancelled"
    assert event["request_id"] == generation_request_id
