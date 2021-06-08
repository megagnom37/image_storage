import asyncio
from hypercorn.asyncio import serve
from hypercorn.config import Config

from .web import app
from .config import IST_SERVICE_HOST, IST_SERVICE_PORT


hypercorn_config = Config.from_mapping(
            bind=f"{IST_SERVICE_HOST}:{IST_SERVICE_PORT}",
            graceful_timeout=0,
        )

asyncio.run(serve(app,
      hypercorn_config,
      shutdown_trigger=asyncio.Future))
