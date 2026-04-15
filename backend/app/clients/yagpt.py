from __future__ import annotations

import asyncio
import time
from typing import Any

import httpx

from app.config.abc import YagptSettings
from app.services.clients.llm import LLMClient, LLMMessage

YAGPT_COMPLETION_ASYNC_URL = (
    "https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync"
)
YAGPT_OPERATIONS_URL = "https://operation.api.cloud.yandex.net/operations"

DEFAULT_POLL_INTERVAL_S = 1.0
DEFAULT_OPERATION_TIMEOUT_S = 120.0


def _extract_answer_text(data: dict[str, Any]) -> str:
    """Ответ completionAsync в поле response: alternatives[0].message.text."""
    if "alternatives" in data:
        return data["alternatives"][0]["message"]["text"]
    res = data.get("result")
    if isinstance(res, dict) and "alternatives" in res:
        return res["alternatives"][0]["message"]["text"]
    msg = f"Unexpected YaGPT response shape: {data!r}"
    raise RuntimeError(msg)


def _http_error_detail(resp: httpx.Response) -> str:
    try:
        return resp.text[:2000]
    except Exception:
        return ""


class YandexFoundationLLMClient(LLMClient):
    def __init__(self, settings: YagptSettings) -> None:
        self._settings = settings
        self._client = httpx.AsyncClient(timeout=120.0)

    def _model_uri(self) -> str:
        if self._settings.model_uri:
            return self._settings.model_uri
        # Как в рабочем тесте: yandexgpt-lite (sync /completion часто отдаёт 500)
        return f"gpt://{self._settings.folder_id}/yandexgpt-lite/latest"

    def _ensure_credentials(self) -> None:
        if not (self._settings.api_key or "").strip():
            msg = "APP_YAGPT__API_KEY пустой — задайте в backend/.env для контейнера"
            raise ValueError(msg)
        if not (self._settings.folder_id or "").strip():
            msg = "APP_YAGPT__FOLDER_ID пустой — задайте в backend/.env для контейнера"
            raise ValueError(msg)

    async def complete(self, system_prompt: str, messages: list[LLMMessage]) -> str:
        self._ensure_credentials()
        body_messages: list[dict[str, Any]] = []
        if system_prompt:
            body_messages.append({"role": "system", "text": system_prompt})
        for m in messages:
            body_messages.append({"role": m.role, "text": m.content})

        payload: dict[str, Any] = {
            "modelUri": self._model_uri(),
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,
                "maxTokens": "2000",
            },
            "messages": body_messages,
        }

        headers = {
            "Authorization": f"Api-Key {self._settings.api_key}",
            "Content-Type": "application/json",
        }

        start = await self._client.post(
            YAGPT_COMPLETION_ASYNC_URL,
            json=payload,
            headers=headers,
        )
        if start.is_error:
            detail = _http_error_detail(start)
            msg = f"YaGPT completionAsync HTTP {start.status_code}: {detail}"
            raise RuntimeError(msg)
        operation = start.json()
        operation_id = operation["id"]

        deadline = time.monotonic() + DEFAULT_OPERATION_TIMEOUT_S
        while time.monotonic() < deadline:
            poll = await self._client.get(
                f"{YAGPT_OPERATIONS_URL}/{operation_id}",
                headers=headers,
            )
            if poll.is_error:
                detail = _http_error_detail(poll)
                msg = f"YaGPT operations GET HTTP {poll.status_code}: {detail}"
                raise RuntimeError(msg)
            status_data = poll.json()
            if not status_data.get("done"):
                await asyncio.sleep(DEFAULT_POLL_INTERVAL_S)
                continue
            if "error" in status_data:
                msg = f"YaGPT operation error: {status_data['error']!r}"
                raise RuntimeError(msg)
            response_obj = status_data.get("response")
            if response_obj is None:
                msg = f"YaGPT operation done but no response: {status_data!r}"
                raise RuntimeError(msg)
            return _extract_answer_text(response_obj)

        msg = (
            f"YaGPT operation {operation_id} timed out "
            f"after {DEFAULT_OPERATION_TIMEOUT_S}s"
        )
        raise TimeoutError(msg)

    async def aclose(self) -> None:
        await self._client.aclose()
