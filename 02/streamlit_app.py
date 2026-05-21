import streamlit as st
import requests

# 기본 UI 설정
st.set_page_config(page_title="FastAPI Test UI", page_icon="🚀", layout="wide")
st.title("🚀 FastAPI Backend Test Dashboard")

# 사이드바: 서버 설정
with st.sidebar:
    st.header("⚙️ Server Settings")
    BASE_URL = st.text_input("API Base URL", value="http://localhost:8000")
    st.info("FastAPI 서버가 실행 중인 주소를 입력하세요.")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📝 게시글 (Posts)", "💬 댓글 (Comments)", "🤖 AI 기능 (LLM)"])

# ==========================================
# 탭 1: 게시글 (Posts) API
# ==========================================
with tab1:
    st.header("게시글 관리")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("새 게시글 작성 (POST)")
        post_title = st.text_input("제목 (title)")
        post_text = st.text_area("내용 (text)")
        post_author = st.text_input("작성자 (author)", key="post_create_author")
        
        if st.button("게시글 생성"):
            payload = {"title": post_title, "text": post_text, "author": post_author} # PostCreate 스키마
            response = requests.post(f"{BASE_URL}/posts/", json=payload)
            if response.status_code == 200:
                st.success("생성 성공!")
                st.json(response.json())
            else:
                st.error(f"오류: {response.status_code} - {response.text}")

        st.divider()

        st.subheader("게시글 목록 조회 (GET)")
        page_idx = st.number_input("페이지 번호", min_value=1, value=1)
        if st.button("목록 불러오기"):
            response = requests.get(f"{BASE_URL}/posts/page/{page_idx}")
            if response.status_code == 200:
                st.json(response.json())
            else:
                st.error(f"오류: {response.status_code}")

    with col2:
        st.subheader("단일 게시글 조회 (GET)")
        read_post_id = st.number_input("조회할 게시글 ID", min_value=1, value=1, key="read_post")
        if st.button("게시글 조회"):
            response = requests.get(f"{BASE_URL}/posts/{read_post_id}")
            if response.status_code == 200:
                st.json(response.json())
            else:
                st.error("게시글을 찾을 수 없거나 오류가 발생했습니다.")

        st.divider()
        
        st.subheader("게시글 수정/삭제")
        action_post_id = st.number_input("대상 게시글 ID", min_value=1, value=1, key="action_post")
        
        with st.expander("게시글 수정하기 (PATCH)"):
            update_title = st.text_input("수정할 제목 (title)", key="update_title")
            update_text = st.text_area("수정할 내용 (text)", key="update_text")
            update_author = st.text_input("작성자 확인 (author)", key="update_author")
            if st.button("게시글 수정"):
                payload = {"title": update_title, "text": update_text, "author": update_author} # PostUpdate 스키마
                response = requests.patch(f"{BASE_URL}/posts/{action_post_id}", json=payload)
                if response.status_code == 200:
                    st.success("수정 완료!")
                else:
                    st.error("수정 실패")
                    
        with st.expander("게시글 삭제하기 (DELETE)"):
            delete_post_author = st.text_input("삭제 권한 확인용 작성자 (author)", key="delete_post_author")
            if st.button("게시글 삭제"):
                payload = {"author": delete_post_author} # PostDelete 스키마
                response = requests.delete(f"{BASE_URL}/posts/{action_post_id}", json=payload) 
                if response.status_code == 200:
                    st.success("삭제 완료!")
                else:
                    st.error("삭제 실패")

# ==========================================
# 탭 2: 댓글 (Comments) API
# ==========================================
with tab2:
    st.header("댓글 관리")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("댓글 작성 (POST)")
        target_post_id = st.number_input("댓글을 달 게시글 ID", min_value=1, value=1)
        comment_text = st.text_area("댓글 내용 (text)")
        comment_author = st.text_input("댓글 작성자 (author)", key="comment_create_author")
        
        if st.button("댓글 작성"):
            payload = {"text": comment_text, "author": comment_author} # CommentCreate 스키마
            response = requests.post(f"{BASE_URL}/posts/{target_post_id}/comments", json=payload)
            if response.status_code == 200:
                st.success("댓글 생성 완료!")
                st.json(response.json())
            else:
                st.error("댓글 생성 실패")

    with col4:
        st.subheader("댓글 조회/수정/삭제")
        target_comment_id = st.number_input("대상 댓글 ID", min_value=1, value=1)
        
        if st.button("댓글 단일 조회 (GET)"):
            response = requests.get(f"{BASE_URL}/comments/{target_comment_id}")
            if response.status_code == 200:
                st.json(response.json())
            else:
                st.error("조회 실패")
                
        with st.expander("댓글 수정하기 (PATCH)"):
            update_comment_text = st.text_input("수정할 댓글 내용 (text)", key="update_comment_text")
            update_comment_author = st.text_input("작성자 확인 (author)", key="update_comment_author")
            if st.button("댓글 수정"):
                payload = {"text": update_comment_text, "author": update_comment_author} # CommentUpdate 스키마
                response = requests.patch(f"{BASE_URL}/comments/{target_comment_id}", json=payload)
                if response.status_code == 200:
                    st.success("수정 완료!")
                else:
                    st.error("수정 실패")
                    
        with st.expander("댓글 삭제하기 (DELETE)"):
            delete_comment_author = st.text_input("삭제 권한 확인용 작성자 (author)", key="delete_comment_author")
            if st.button("댓글 삭제"):
                payload = {"author": delete_comment_author} # CommentDelete 스키마
                response = requests.delete(f"{BASE_URL}/comments/{target_comment_id}", json=payload)
                if response.status_code == 200:
                    st.success("삭제 완료!")
                else:
                    st.error("삭제 실패")

# ==========================================
# 탭 3: AI 기능 (LLM Streaming)
# ==========================================
with tab3:
    st.header("AI 요약 및 번역 (Streaming Test)")
    
    llm_post_id = st.number_input("작업할 게시글 ID", min_value=1, value=1, key="llm_post")
    
    st.divider()
    
    st.subheader("🌐 게시글 번역")
    target_language = st.selectbox("목표 언어", ["Korean", "English", "Japanese", "Spanish", "French"])
    
    if st.button("번역 시작"):
        result_box = st.empty()
        full_text = ""
        
        try:
            with requests.get(f"{BASE_URL}/posts/{llm_post_id}/translation/{target_language}", stream=True) as r:
                r.raise_for_status()
                for line in r.iter_lines(decode_unicode=True):
                    if line:
                        if line.startswith("data: "):
                            chunk = line[6:]
                            if chunk and chunk != "[DONE]":
                                # 💡 핵심 수정 포인트: 이스케이프된 줄바꿈 문자를 실제 줄바꿈으로 치환
                                chunk = chunk.replace('\\n', '\n')
                                full_text += chunk
                                result_box.markdown(full_text + "▌")
                                
                result_box.markdown(full_text)
                st.success("번역 완료!")
        except Exception as e:
            st.error(f"요청 중 오류가 발생했습니다: {e}")

    st.divider()

    st.subheader("✨ 게시글 요약")
    if st.button("요약 시작"):
        result_box = st.empty()
        full_text = ""
        
        try:
            with requests.get(f"{BASE_URL}/posts/{llm_post_id}/summarization", stream=True) as r:
                r.raise_for_status()
                for line in r.iter_lines(decode_unicode=True):
                    if line:
                        if line.startswith("data: "):
                            chunk = line[6:]
                            if chunk and chunk != "[DONE]":
                                # 💡 핵심 수정 포인트: 이스케이프된 줄바꿈 문자를 실제 줄바꿈으로 치환
                                chunk = chunk.replace('\\n', '\n')
                                full_text += chunk
                                result_box.markdown(full_text + "▌")
                                
                result_box.markdown(full_text)
                st.success("요약 완료!")
        except Exception as e:
            st.error(f"요청 중 오류가 발생했습니다: {e}")