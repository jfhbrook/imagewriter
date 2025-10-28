from abc import ABC, abstractmethod
from concurrent.futures import Executor
import logging
import queue
import time
from typing import Any, Callable, List, Optional, Self, Sequence

from imagewriter.encoding import Command
from imagewriter.serial import Serial, SerialProtocol

logger = logging.getLogger(__name__)


class Request(queue.Queue[Any], ABC):
    def __init__(self: Self, command: Any) -> None:
        self.command = command

    def result(self: Self, timeout: Optional[float] = None) -> Any:
        """
        Get the result of a request. Blocks until results are complete,
        barring a timeout.
        """

        res = self.get(timeout=timeout)

        if isinstance(res, Exception):
            raise res

        return res


class WriteRequest(Request):
    """
    A request to write a Command.
    """

    pass


class FlushRequest(Request):
    """
    A request to flush the connection.
    """

    def __init__(self: Self) -> None:
        super().__init__(None)


class InterruptRequest(Request):
    """
    A request to interrupt with multiple commands.
    """

    pass


class Response(ABC):
    @abstractmethod
    def result(self: Self, timeout: Optional[float] = None) -> Any:
        raise NotImplementedError("Response.result")


class WriteResponse(Response):
    """
    A response to a write request.
    """

    def __init__(self: Self, requests: Sequence[Request]) -> None:
        self._requests = requests

    def result(self: Self, timeout: Optional[float] = None) -> Any:
        count: Optional[int] = None

        for req in self._requests:
            res = req.result(timeout=timeout)
            if res is not None:
                if count is None:
                    count = 0
                count += res

        return count


class InterruptResponse(Response):
    """
    A response to an interrupt request.
    """

    def __init__(self: Self, request: InterruptRequest) -> None:
        self._request = request

    def result(self: Self, timeout: Optional[float] = None) -> Any:
        count: Optional[int] = None

        for res in self._request.result(timeout=timeout):
            if res is not None:
                if count is None:
                    count = 0
                count += res

        return count


class InterruptError(Exception):
    """
    An exception raised when a command is interrupted.
    """

    pass


def _get_request(connection: "Connection") -> Request:
    """
    Get the next request, respecting interrupts.
    """

    try:
        return connection._interrupt_queue.get_nowait()
    except queue.Empty:
        pass

    req = connection._request_queue.get()

    while not connection.serial.cts:
        try:
            return connection._interrupt_queue.get_nowait()
        except queue.Empty:
            pass

        time.sleep(1 / connection.serial.baudrate)

    return req


def _get_request_nowait(connection: "Connection") -> Request:
    """
    Get the next request if available, respecting interrupts. Do not wait for
    CTS to be asserted.
    """

    req = connection._request_queue.get_nowait()

    try:
        return connection._interrupt_queue.get_nowait()
    except queue.Empty:
        pass

    return req


def _write(connection: "Connection", request: WriteRequest) -> None:
    """
    Write a command to the serial port.
    """

    res = connection.serial.write(bytes(request.command))
    request.put(res)


def _flush(connection: "Connection", request: FlushRequest) -> None:
    """
    Write any remaining commands, and flush the connection.
    """

    requests: List[FlushRequest] = [request]

    try:
        while True:
            req = _get_request_nowait(connection)
            if isinstance(req, FlushRequest):
                requests.append(req)
            else:
                assert isinstance(req, WriteRequest)
                res = _write(connection, req)
                req.put(res)
    except queue.Empty:
        pass
    except Exception as exc:
        for req in requests:
            req.put(exc)
        for req in _dump(connection):
            req.put(exc)
        return

    connection.flush()

    for req in requests:
        req.put(None)


def _interrupt(connection: "Connection", request: InterruptRequest) -> None:
    """
    Temporarily disable flow control, run interrupt commands, and dump the
    remaining commands.
    """

    try:
        connection.set_flow_control(False)

        result = [
            connection.serial.write(bytes(command)) for command in request.command
        ]

        connection.serial.flush()

        connection.set_flow_control(True)

        for res in _dump(connection):
            res.put(InterruptError(f"Command was interrupted with: {request.command}"))
    except Exception as exc:
        request.put(exc)
    else:
        request.put(result)


def _dump(connection: "Connection") -> List[Request]:
    """
    Dump and return remaining requests.
    """

    requests: List[Request] = list()

    try:
        while True:
            req = connection._request_queue.get_nowait()
            requests.append(req)
    except queue.Empty:
        pass

    return requests


def _worker(connection: "Connection") -> Callable[[], None]:
    def worker() -> None:
        while connection._running:
            try:
                request = _get_request(connection)

                try:
                    if isinstance(request, InterruptRequest):
                        _interrupt(connection, request)
                    elif isinstance(request, FlushRequest):
                        _flush(connection, request)
                    else:
                        assert isinstance(request, WriteRequest)
                        _write(connection, request)
                except Exception as exc:
                    request.put(exc)
            except queue.Empty:
                # No ready command - that's OK
                continue
            except Exception as exc:
                logger.error(exc)

    return worker


class Connection:
    def __init__(self: Self, serial: Serial, executor: Executor) -> None:
        self.serial: Serial = serial
        self._executor: Executor = executor
        self._request_queue: queue.Queue[Request] = queue.Queue(maxsize=0)
        self._interrupt_queue: queue.Queue[InterruptRequest] = queue.Queue()

        self._running: bool = True
        self._executor.submit(_worker(self))

    def write(self: Self, commands: Sequence[Command]) -> WriteResponse:
        requests = [WriteRequest(command) for command in commands]

        for req in requests:
            self._request_queue.put(req)

        return WriteResponse(requests)

    def interrupt(self: Self, commands: Sequence[Command]) -> Response:
        interrupt = InterruptRequest(list(commands))
        self._interrupt_queue.put_nowait(interrupt)

        return InterruptResponse(interrupt)

    def flush(self: Self) -> None:
        req = FlushRequest()
        self._request_queue.put(req)
        return req.result()

    def set_flow_control(self: Self, enabled: bool) -> None:
        if self.serial.protocol == SerialProtocol.XONXOFF:
            self.serial.xonxoff = enabled
        else:
            self.serial.rtscts = enabled

    def stop(self: Self) -> None:
        self._running = False
