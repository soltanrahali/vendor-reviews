import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.title("Vendor Reviews")

# --- Sidebar: create a vendor ---
with st.sidebar:
    st.header("New Vendor")
    new_vendor = st.text_input("Vendor name")
    if st.button("Create"):
        r = requests.post(f"{API_URL}/vendors", json={"name": new_vendor})
        if r.status_code == 200:
            st.success(f"'{new_vendor}' created!")
            st.rerun()
        else:
            st.error(r.json().get("detail", "Error"))

# --- Main: pick vendor ---
vendors_r = requests.get(f"{API_URL}/vendors")
vendors = vendors_r.json() if vendors_r.ok else []

if not vendors:
    st.info("No vendors yet — add one in the sidebar.")
    st.stop()

vendor_map = {v["name"]: v["id"] for v in vendors}
selected = st.selectbox("Select a vendor", list(vendor_map.keys()))
vendor_id = vendor_map[selected]

tab_comment, tab_summary = st.tabs(["Add Comment", "Summary"])

with tab_comment:
    text = st.text_area("Your comment")
    if st.button("Submit Comment"):
        if not text.strip():
            st.warning("Please write something first.")
        else:
            r = requests.post(
                f"{API_URL}/vendors/{vendor_id}/comments", json={"content": text}
            )
            if r.ok:
                data = r.json()
                sentiment_emoji = {"positive": "😊", "negative": "😟", "neutral": "😐"}.get(
                    data["sentiment"], ""
                )
                st.success(f"Added! Sentiment: {data['sentiment']} {sentiment_emoji}")
            else:
                st.error(r.json().get("detail", "Error"))

with tab_summary:
    if st.button("Generate Summary"):
        r = requests.get(f"{API_URL}/vendors/{vendor_id}/summary")
        if r.ok:
            data = r.json()
            st.subheader(f"{data['vendor']} — {data['total_comments']} comment(s)")
            st.write(data["summary"])
        else:
            st.error("Could not generate summary.")
