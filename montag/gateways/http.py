from typing import Optional, Protocol


class HttpResponse(Protocol):
    status_code: int

    def json(self) -> dict:
        ...


class HttpAdapter(Protocol):
    def get(
        self,
        url: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> HttpResponse:
        ...

    def post(
        self,
        url: str,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> HttpResponse:
        ...
