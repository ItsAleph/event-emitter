import asyncio
from typing import Dict, List

class EventEmitter:
    """
    General-purpose, context-agnostic, simple (a)synchronous pub-sub system.

    Parameters
    ----------
    strict: :class:`bool`
        Whether this emitter is strict. If emitter is strict, attempt to
        register asynchronous listener for event and then emit it using
        :meth:`emit_sync` will result in an error. If emitter is not strict,
        such attempt will only result in :class:`RuntimeWarning` and not
        calling the listener.

    Attributes
    ----------
    strict: :class:`bool`
        Whether this emitter is strict. See above for details.
    listeners: Dict[:class:`str`, List]
        Mapping of event names to their listener list.
    """
    def __init__(self, strict: bool = True) -> None:
        self.strict: bool = True
        self.listeners: Dict[str, List] = {}

    def listen(self, event: str):
        """
        Registers a listener for the specified event.
        
        Parameters
        ----------
        event: :class:`str`
            The name of the event to listen.
        """
        def decorator(func):
            if lsrns := self.listeners.get(event):
                lsrns.append(func)
            else:
                self.listeners[event] = [func]

            return func

        return decorator

    async def emit_async(self, event: str, *args, **kwargs):
        """
        Emits event with the given parameters, awaiting all
        async listeners.

        Parameters
        ----------
        event: :class:`str`
            The event to emit.
        *args: Any
            Positional arguments to pass into listeners.
        **kwargs: Any
            Keyword arguments to pass into listeners.
        """
        for listener in self._listeners.get(event, []):
            if asyncio.iscoroutinefunction(listener):
                await listener(*args, **kwargs)
            else:
                listener(*args, **kwargs)

    async def emit_sync(self, event: str, *args, **kwargs):
        """
        Emits event eith the given parameters.

        Parameters
        ----------
        event: :class:`str`
            The event to emit.
        *args: Any
            Positional arguments to oass into listeners.
        **kwargs: Any
            Keyword arguments to pass into listeners.

        Raises
        ------
        RuntimeError
            Attempt to run asynchronous listener was made
            and :attr:`strict` is `True`
        