from litestar import Request, post
from litestar.exceptions import HTTPException, ServiceUnavailableException
from pydantic import BaseModel, Field

from app.services.clients.llm import LLMMessage


class LlmDirectBody(BaseModel):
    message: str = Field(..., min_length=1)
    system_prompt: str | None = None


@post("/llm/complete")
async def llm_complete(data: LlmDirectBody, request: Request) -> dict[str, str]:
    llm = request.app.state.llm_client
    if llm is None:
        raise ServiceUnavailableException(
            detail="LLM не настроен (профиль dummy или клиент не инициализирован)",
        )
    system = data.system_prompt or ""
    try:
        text = await llm.complete(
            system,
            [LLMMessage(role="user", content=data.message)],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except (RuntimeError, TimeoutError) as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
    return {"text": text}
