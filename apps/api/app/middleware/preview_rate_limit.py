import time
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Tuple

class PreviewRateLimitMiddleware(BaseHTTPMiddleware):
    # Store IP -> (request_count, window_start_time)
    _rate_limits: Dict[str, Tuple[int, float]] = {}
    LIMIT = 10  # max 10 requests per minute
    WINDOW = 60.0  # window duration in seconds

    async def dispatch(self, request: Request, call_next):
        # Apply rate limiting to the public preview routes
        if request.url.path.startswith("/api/public-preview"):
            client_ip = request.client.host if request.client else "unknown"
            current_time = time.time()
            
            if client_ip not in self._rate_limits:
                self._rate_limits[client_ip] = (1, current_time)
            else:
                count, start_time = self._rate_limits[client_ip]
                if current_time - start_time > self.WINDOW:
                    # Reset window
                    self._rate_limits[client_ip] = (1, current_time)
                else:
                    if count >= self.LIMIT:
                        return JSONResponse(
                            status_code=429,
                            content={"detail": "Too many requests. Please wait before asking again."}
                        )
                    self._rate_limits[client_ip] = (count + 1, start_time)

        return await call_next(request)
