from __future__ import annotations

import streamlit as st

from ollama_client import OllamaClient
from prompts import build_cleanup_prompt, build_ocr_prompt
from utils import ensure_nonempty_message, image_file_to_base64, normalize_output


st.set_page_config(page_title="손글씨 OCR (Ollama qwen3-vl:4b)", page_icon="📝", layout="centered")

MODEL_NAME = "qwen3-vl:4b"

st.title("📝 손글씨 이미지 → 텍스트 변환")
st.caption("로컬 Ollama(qwen3-vl:4b) 기반으로 손글씨를 텍스트로 변환합니다.")

with st.sidebar:
    st.header("설정")
    ollama_url = st.text_input("Ollama Endpoint", value="http://localhost:11434")
    timeout_sec = st.slider("요청 타임아웃(초)", min_value=30, max_value=300, value=120, step=10)

client = OllamaClient(base_url=ollama_url, timeout=timeout_sec)

st.subheader("1) 연결 상태")
status = client.check_status(MODEL_NAME)
if status.server_ok:
    st.success("✅ Ollama 서버 연결 성공")
else:
    st.error(f"❌ {status.message}")

if status.server_ok and status.model_available:
    st.success(f"✅ 모델 준비됨: {MODEL_NAME}")
elif status.server_ok:
    st.warning(f"⚠️ {status.message}")

st.subheader("2) 업로드")
uploaded = st.file_uploader("손글씨 이미지를 업로드하세요", type=["jpg", "jpeg", "png", "webp"])

language = st.selectbox("언어 선택", options=["한국어", "영어", "혼합"], index=0)
output_mode = st.radio("출력 모드", options=["원문 그대로(줄바꿈 유지)", "정리(맞춤법/띄어쓰기 개선)"], index=0)
preserve_layout = st.checkbox("서식 유지(가능한 줄바꿈 유지)", value=True)

if uploaded is not None:
    st.image(uploaded, caption="업로드 이미지 미리보기", use_container_width=True)

st.subheader("3) 변환 실행")
run = st.button("텍스트로 변환", type="primary", disabled=uploaded is None)

if run:
    if not status.server_ok:
        st.error("Ollama 서버에 연결되지 않았습니다. `ollama serve` 실행 상태를 확인해주세요.")
    elif not status.model_available:
        st.error(f"모델이 준비되지 않았습니다. `ollama pull {MODEL_NAME}` 후 다시 시도해주세요.")
    else:
        try:
            image_b64, _ = image_file_to_base64(uploaded)
            ocr_prompt = build_ocr_prompt(language=language, preserve_line_breaks=preserve_layout)

            with st.spinner("이미지에서 글자를 읽는 중..."):
                raw_result = client.generate_with_image(
                    model=MODEL_NAME,
                    prompt=ocr_prompt,
                    image_b64=image_b64,
                    stream=False,
                )

            result_text = normalize_output(raw_result)

            if output_mode == "정리(맞춤법/띄어쓰기 개선)" and result_text.strip():
                cleanup_prompt = build_cleanup_prompt(language)
                with st.spinner("맞춤법/띄어쓰기 정리 중..."):
                    result_text = client.generate_with_image(
                        model=MODEL_NAME,
                        prompt=cleanup_prompt,
                        image_b64=image_b64,
                        stream=False,
                        context_text=f"[OCR 원문]\n{result_text}",
                    )
                result_text = normalize_output(result_text)

            result_text = ensure_nonempty_message(result_text)

            st.text_area("인식 결과", value=result_text, height=320)
            st.info("복사는 결과 텍스트를 선택한 뒤 Ctrl/Cmd + C 로 진행해주세요.")
            st.download_button(
                "txt 다운로드",
                data=result_text.encode("utf-8"),
                file_name="ocr_result.txt",
                mime="text/plain",
            )
            st.caption("⚠️ 개인정보가 포함될 수 있으니 공유 전에 반드시 내용을 확인하세요.")
            st.caption("현재는 이미지 1장씩 처리합니다. 추후 멀티 업로드 확장이 가능합니다.")

        except Exception as exc:
            st.error(f"변환 중 오류가 발생했습니다: {exc}")
