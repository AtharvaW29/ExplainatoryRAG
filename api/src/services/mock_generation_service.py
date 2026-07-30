import asyncio
from collections.abc import AsyncIterator


class MockGenerationService:
    def __init__(self, delay_seconds: float = 0.15) -> None:
        self._delay_seconds = delay_seconds

    async def stream(
        self,
        prompt: str,
    ) -> AsyncIterator[str]:
        response = (
            f"This is a mocked streamed response to your message: {prompt}"
        )

        for word in response.split():
            await asyncio.sleep(self._delay_seconds)
            yield f"{word} "
