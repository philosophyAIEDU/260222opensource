# 손글씨 OCR Streamlit 앱 (Ollama + qwen3-vl:4b)

로컬에서 실행 중인 Ollama의 `qwen3-vl:4b` 모델을 사용해 손글씨 이미지를 텍스트로 변환하는 Streamlit 앱입니다.

## 기능
- Ollama 서버 연결 상태 확인
- `qwen3-vl:4b` 모델 존재 여부 확인
- 손글씨 이미지 업로드(jpg/png/webp) 및 미리보기
- 언어 선택(한국어/영어/혼합)
- 출력 모드
  - 원문 그대로(가능한 줄바꿈 유지)
  - 정리(맞춤법/띄어쓰기 개선)
- 텍스트 결과 표시 + txt 다운로드
- 인식 실패 시 쉬운 안내 메시지 출력

## 프로젝트 구조
- `app.py`: Streamlit UI 및 실행 흐름
- `ollama_client.py`: Ollama HTTP API 호출 래퍼
- `prompts.py`: OCR/정리 프롬프트 템플릿
- `utils.py`: 이미지 base64 변환, 결과 후처리
- `requirements.txt`: 의존성

## 사전 준비
1. Ollama 설치
2. Ollama 실행

```bash
ollama serve
```

3. 모델 다운로드

```bash
ollama pull qwen3-vl:4b
```

## 실행 방법
Python 3.10+ 환경에서:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

브라우저가 열리면 이미지를 업로드하고 **텍스트로 변환** 버튼을 눌러 결과를 확인하세요.

## 참고
- 기본 Ollama endpoint는 `http://localhost:11434`입니다.
- 결과에는 개인정보가 포함될 수 있으니 공유 전에 확인하세요.
- 현재는 1장씩 처리하며, 멀티 업로드는 추후 확장 포인트입니다.
