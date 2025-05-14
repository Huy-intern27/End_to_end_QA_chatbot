import streamlit as st
import requests
from urllib.parse import urljoin

API_BASE = "https://096e-34-73-105-169.ngrok-free.app/search"

st.title("QA Chatbot Search")

question = st.text_input("Nhập câu hỏi của bạn:")
top_k = st.slider("Số kết quả trả về", 1, 5, 3)

if st.button("Tìm kiếm"):
    if question:
        try:
            response = requests.post(
                urljoin(API_BASE, "/search"),
                json={"question": question, "top_k": top_k},
                timeout=30
            )

            if response.status_code == 200:
                results = response.json()['results']
                for i, result in enumerate(results, 1):
                    with st.expander(f"Kết quả {i} (Độ tin cậy: {result['confidence']:.2f})"):
                        st.markdown(f"**Câu trả lời:** {result['answer']}")
                        st.markdown(f"**Độ phù hợp:** `{result['score']:.4f}`")
                        st.markdown("**Ngữ cảnh:**")
                        st.info(result['context'])
            else:
                st.error(f"Lỗi API: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Lỗi kết nối: {str(e)}")
    else:
        st.warning("Vui lòng nhập câu hỏi")
