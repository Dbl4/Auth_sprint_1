from typing import Optional

from services.base import AsyncSearchEngine

es: Optional[AsyncSearchEngine] = None


async def get_async_search() -> AsyncSearchEngine:
    return es
