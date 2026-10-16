"""Order events for the WebSocket endpoint (R9).

The shop operations run in worker threads. The WebSocket connections run in the event loop.
publish() hands each event to the event loop of each subscriber in a thread-safe way.
"""

import asyncio
import threading
from dataclasses import dataclass
from typing import Any

from app.store import User


@dataclass(eq=False)
class Subscriber:
    loop: asyncio.AbstractEventLoop
    queue: asyncio.Queue[dict[str, Any]]
    user_id: int
    sees_all: bool


class EventHub:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._subscribers: list[Subscriber] = []

    def subscribe(self, user: User) -> Subscriber:
        subscriber = Subscriber(asyncio.get_running_loop(), asyncio.Queue(), user.id, user.is_admin)
        with self._lock:
            self._subscribers.append(subscriber)
        return subscriber

    def unsubscribe(self, subscriber: Subscriber) -> None:
        with self._lock:
            if subscriber in self._subscribers:
                self._subscribers.remove(subscriber)

    def publish(self, event: dict[str, Any], owner_id: int) -> None:
        with self._lock:
            targets = [s for s in self._subscribers if s.sees_all or s.user_id == owner_id]
        for subscriber in targets:
            subscriber.loop.call_soon_threadsafe(subscriber.queue.put_nowait, event)


hub = EventHub()
