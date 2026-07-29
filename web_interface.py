#!/usr/bin/env python3
import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Alternative Lifestyle AI",
    page_icon="💊",
    layout="wide"
)

st.markdown("""
<style>
    .pasteur-quote {
        position: fixed; bottom: 20px; right: 20px; font-style: italic; 
        color: #666; font-size: 0.85rem; max-width: 300px; text-align: right;
        opacity: 0.7; z-index: 100;
    }
    .category-badge {
        display: inline-block; padding: 0.2rem 0.5rem; border-radius: 0.25rem;
        font-size: 0.75rem; font-weight: bold; margin-right: 0.5rem;
    }
    .cat-diet { background: #d4edda; color: #155724; }
    .cat-looksmaxxing { background: #cce5ff; color: #004085; }
    .cat-pharmacology { background: #fff3cd; color: #856404; }
    .cat-blackpill { background: #f8d7da; color: #721c24; }
    .cat-bimbofication { background: #ffc0cb; color: #800080; }
    .cat-fitness { background: #a8e6cf; color: #006633; }
    .cat-research { background: #d8b4fe; color: #581c87; }
    .last-resort-notice {
        background: #fff3cd; padding: 8px; border-radius: 4px; margin: 10px 0;
        font-size: 0.85rem; border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "fast"

MODES = {
    "fast": {"name": "Fast", "icon": "⚡", "desc": "Instant answers"},
    "deep": {"name": "Deep Research", "icon": "🔬", "desc": "Live web search"},
    "youtube": {"name": "YouTube", "icon": "📹", "desc": "Video transcripts"}
}

st.title("💊 Alternative Lifestyle AI")
st.markdown('<div class="pasteur-quote">Bernard was right. The microbe is nothing, the terrain is everything.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Mode")
    for mode_id, mode in MODES.items():
        if st.button(f"{mode['icon']} {mode['name']}", use_container_width=True):
            st.session_state.current_mode = mode_id
    st.markdown("---")
    st.markdown("### Settings")
    max_results = st.slider("Max results", 1, 10, 5)
    max_tokens = st.slider("Max tokens", 128, 2048, 512)
    if st.session_state.current_mode == "fast":
        category = st.selectbox("Category:", ["All"] + [
            "diet", "looksmaxxing", "pharmacology", "blackpill",
            "bimbofication", "fitness", "research"
        ])
    else:
        category = None
    show_images = st.checkbox("Show Images", value=True)
    max_images = st.slider("Max Images", 0, 10, 3)
    if st.button("Clear Chat"):
        st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and message.get("used_last_resort", False):
            st.markdown('<div class="last-resort-notice">⚠️ Last resort sources used. Faustian approach maintained.</div>', unsafe_allow_html=True)
        st.markdown(message["content"])
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("Sources"):
                for src in message["sources"]:
                    cat = src.get('category', 'general')
                    cat_class = f"cat-{cat.replace('_', '-')}"
                    lr = " [LAST RESORT]" if src.get('last_resort') else ""
                    st.markdown(f'<span class="category-badge {cat_class}">{cat.upper()}</span> [{src.get("title", "No title")}]({src.get("url", "")}){lr}', unsafe_allow_html=True)

if prompt := st.chat_input("Ask about diet, looksmaxxing, pharmacology..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            data = {
                "query": prompt,
                "mode": st.session_state.current_mode,
                "max_results": max_results,
                "max_tokens": max_tokens,
                "include_images": show_images,
                "image_limit": max_images
            }
            if st.session_state.current_mode == "fast" and category and category != "All":
                data["filter_source"] = category
            if show_images:
                response = requests.post(f"{API_URL}/query_with_images", json=data, timeout=60)
            else:
                response = requests.post(f"{API_URL}/query", json=data, timeout=60)
            if response.status_code == 200:
                result = response.json()
                placeholder.markdown(result["answer"])
                message_data = {
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"]
                }
                if "used_last_resort" in result:
                    message_data["used_last_resort"] = result["used_last_resort"]
                if show_images and "images" in result and result["images"]:
                    message_data["images"] = result["images"]
                st.session_state.messages.append(message_data)
        except Exception as e:
            placeholder.error(str(e))

st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>Alternative Lifestyle AI - Personal Knowledge System</p>", unsafe_allow_html=True)