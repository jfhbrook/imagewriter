import asyncio


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    # Read and write from an open client connection
    pass


async def server(host: str = "localhost", port: int = 9100) -> asyncio.Server:
    return await asyncio.start_server(handler, host, port)
