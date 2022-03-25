from typing import Optional, Protocol

import requests


class HttpResponse(Protocol):
    status_code: int

    def json(self) -> dict:
        ...

    @property
    def text(self) -> str:
        ...


class HttpAdapter:
    def get(
        self, url: str, params: Optional[dict] = None, headers: Optional[dict] = None
    ) -> HttpResponse:
        return requests.get(url, params=params, headers=headers)

    def post(
        self,
        url: str,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> HttpResponse:
        return requests.post(url, data=data, json=json, headers=headers)

    def put(
        self,
        url: str,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> HttpResponse:
        return requests.put(url, data=data, json=json, headers=headers)
