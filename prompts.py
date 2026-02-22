"""Prompt templates for handwriting OCR and optional text cleanup."""

from __future__ import annotations


def build_ocr_prompt(language: str, preserve_line_breaks: bool) -> str:
    language_map = {
        "한국어": "한국어",
        "영어": "영어",
        "혼합": "한국어와 영어 혼합",
    }
    language_instruction = language_map.get(language, "한국어와 영어 혼합")

    line_break_instruction = (
        "원문 줄바꿈과 문단을 가능한 한 그대로 유지해라."
        if preserve_line_breaks
        else "줄바꿈은 필수적인 경우에만 사용하고 읽기 쉬운 plain text로 출력해라."
    )

    return f"""
너는 OCR(문자인식) 도우미다.
이미지의 손글씨를 가능한 정확히 텍스트로 옮겨 적어라.
출력은 텍스트만 작성하고 설명, 해석, 요약, 주석을 절대 추가하지 마라.
확실하지 않은 문자나 단어는 [[불명확]]로 표시해라.
임의로 문장이나 단어를 만들어내지 마라.
요청 언어는 {language_instruction}다. 원문이 혼합 언어면 그대로 유지해라.
{line_break_instruction}
""".strip()


def build_cleanup_prompt(language: str) -> str:
    language_map = {
        "한국어": "한국어",
        "영어": "영어",
        "혼합": "한국어/영어 혼합",
    }
    language_instruction = language_map.get(language, "한국어/영어 혼합")

    return f"""
너는 텍스트 정리 도우미다.
아래 OCR 결과를 보고 맞춤법/띄어쓰기만 개선해라.
의미를 변경하거나 내용을 추가/삭제/요약하지 마라.
고유명사, 숫자, 기호, 줄 번호, 목록 표시는 최대한 보존해라.
읽을 수 없는 표시([[불명확]])는 그대로 유지해라.
출력은 텍스트만 작성해라.
언어 기준: {language_instruction}
""".strip()
