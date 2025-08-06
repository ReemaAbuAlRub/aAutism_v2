# File: streamlit_app.py

import streamlit as st
import requests
import base64
from typing import Optional
from io import BytesIO


API_URL = "http://localhost:8000/api/v1"


def register_user(email: str, password: str) -> dict:
    resp = requests.post(
        f"{API_URL}/user/register",
        json={"email": email, "password": password},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def login_user(email: str, password: str) -> Optional[str]:
    data = {
        "grant_type": "password",
        "username": email,
        "password": password,
    }
    resp = requests.post(
        f"{API_URL}/user/login",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=60,
    )
    if resp.status_code == 200:
        return resp.json().get("access_token")
    return None


def send_message(token: str, text: str, generate_image: bool) -> dict:
    # increase timeout to 60s; you can also remove it if you prefer no limit
    try:
        resp = requests.post(
            f"{API_URL}/chat",
            json={"text": text, "generate_image": generate_image},
            headers={"Authorization": f"Bearer {token}"}
        )
    except requests.exceptions.ReadTimeout:
       raise RuntimeError(
            "The request timed out after 60 seconds. "
            "The bot may be taking longer (e.g. generating an image or TTS). "
            "Please try again or disable image generation."
        )
    resp.raise_for_status()
    return resp.json()


def logout():
    st.session_state.clear()
    # no explicit rerun needed—widget events auto-rerun


def show_auth_page():
    st.sidebar.header("Authenticate")
    mode = st.sidebar.radio("Mode", ["Login", "Register"])
    with st.form("auth_form"):
        email = st.text_input("Email", key="auth_email")
        password = st.text_input("Password", type="password", key="auth_pw")
        submitted = st.form_submit_button(mode)
        if submitted:
            try:
                if mode == "Register":
                    register_user(email, password)
                    st.success("Registration successful! Please log in.")
                else:
                    token = login_user(email, password)
                    if token:
                        st.session_state.token = token
                        st.success("Logged in successfully.")
                        # next widget event (any) will rerun script
                    else:
                        st.error("Invalid credentials.")
            except requests.HTTPError as e:
                detail = e.response.json().get("detail", str(e))
                st.error(f"{mode} failed: {detail}")


def show_chat_page():
    st.sidebar.button("Logout", on_click=logout)
    st.sidebar.write("Logged in ✅")

    st.subheader("Chat")
    generate_image = st.checkbox("Generate Image")
    user_input = st.text_input("You:", key="chat_input")

    if st.button("Send"):
        try:
            result = send_message(st.session_state.token, user_input, generate_image)
            st.markdown(f"**Assistant:** {result['text']}")

            audio_bytes = base64.b64decode(result["audio_base64"])
            st.audio(audio_bytes, format="audio/mp3")

            img_b64 = result.get("image_url")
            if img_b64:
                # 1) If your API is returning a data-URI prefix, strip it:
                if img_b64.startswith("data:image"):
                    img_b64 = img_b64.split(",", 1)[1]

                # 2) Decode the base64 string
                img_bytes = base64.b64decode(img_b64)

                # 3) Wrap in a BytesIO and display
                img_buffer = BytesIO(img_bytes)
                st.image(img_buffer, caption="Generated image", use_column_width=True)
            else:
                st.write("No image was returned from the API.")
        except requests.HTTPError as e:
            detail = e.response.json().get("detail", str(e))
            st.error(f"Chat error: {detail}")


def main():
    st.set_page_config(page_title="Autism ChatBot", layout="wide")
    st.title("Autism ChatBot")

    # Initialize token in session state
    if "token" not in st.session_state:
        st.session_state.token = None

    # Branch between auth & chat
    if not st.session_state.token:
        show_auth_page()
    else:
        show_chat_page()


if __name__ == "__main__":
    main()
