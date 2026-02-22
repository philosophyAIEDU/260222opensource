"""Simple Ollama HTTP client wrapper for vision OCR use-case."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class OllamaStatus:
    server_ok: bool
    model_available: bool
    message: str


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = 120):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def check_status(self, model: str) -> OllamaStatus:
        try:
            tags_resp = requests.get(f"{self.base_url}/api/tags", timeout=10)
            tags_resp.raise_for_status()
        except requests.RequestException as exc:
            return OllamaStatus(
                server_ok=False,
                model_available=False,
                message=f"Ollama 서버에 연결할 수 없습니다: {exc}",
            )

        models = tags_resp.json().get("models", [])
        model_names = {m.get("name", "") for m in models}
        if model in model_names:
            return OllamaStatus(True, True, f"Ollama 연결 성공 / 모델 확인됨: {model}")

        return OllamaStatus(
            server_ok=True,
            model_available=False,
            message=f"모델이 없습니다: {model}. 터미널에서 `ollama pull {model}`을 실행하세요.",
        )

    def generate_with_image(
        self,
        model: str,
        prompt: str,
        image_b64: str,
        stream: bool = False,
        context_text: Optional[str] = None,
    ) -> str:
        payload = {
            "model": model,
            "prompt": f"{prompt}\n\n{context_text}" if context_text else prompt,
            "images": [image_b64],
            "stream": stream,
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
                stream=stream,
            )
            response.raise_for_status()
        except requests.Timeout as exc:
            raise RuntimeError("요청 시간이 초과되었습니다. 이미지 크기를 줄이거나 다시 시도해주세요.") from exc
        except requests.RequestException as exc:
            raise RuntimeError(f"Ollama 요청 중 오류가 발생했습니다: {exc}") from exc

        if stream:
            chunks = []
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    data = requests.models.complexjson.loads(line)
                    if "response" in data:
                        chunks.append(data["response"])
                except Exception:
                    continue
            return "".join(chunks)

        data = response.json()
        return data.get("response", "")
