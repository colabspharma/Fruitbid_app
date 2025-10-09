# =====================================================
# 🍎 app_web.py — Main FruitBid App Entry Point (clean version)
# =====================================================

import os
import sqlite3
from datetime import datetime
import streamlit as st
from supabase import create_client

# =====================================================
# ✅ PAGE CONFIG (must be first Streamlit call)
# =====================================================
try:
    st.set_page_config(
        page_title="🍎 FruitBid App",
        page_icon="🍇",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception:
    pass  # Ignore if already set (e.g. hot reload)

# =====================================================
# 🌐 SUPABASE CONNECTION
# =====================================================
if "supabase" not in st.secrets:
    st.error("❌ Could not load Supabase secrets. Check `.streamlit/secrets.toml` inside your FruitBidApp folder.")
    st.stop()

# --- Load Supabase credentials ---
try:
    supabase_url = st.secrets["supabase"]["url"]
    supabase_key = (
        st.secrets["supabase"].get("anon_key")
        or st.secrets["supabase"].get("key")
    )

    if not supabase_url or not supabase_key:
        raise KeyError("Missing Supabase URL or key")
except Exception as e:
    st.error(f"❌ Could not load Supabase credentials: {e}")
    st.stop()

# Debug info
st.write("🔍 Supabase URL:", supabase_url)
st.write("🔑 Key starts with:", supabase_key[:8] + "...")

# --- Initialize client ---
try:
    supabase = create_client(supabase_url, supabase_key)
except Exception as e:
    st.warning(f"⚠️ Supabase client not initialized: {e}")
    supabase = None

# =====================================================
# 📂 SIDEBAR
# =====================================================
try:
    from components.sidebar import render_sidebar
except ModuleNotFoundError:
    def render_sidebar():
        with st.sidebar:
            return st.radio(
                "Navigate:",
                ["🏠 Home", "🏪 Marketplace", "💼 My Bids", "⚙️ Add Lot (Admin)"]
            )
    st.warning("⚠️ Sidebar missing — using fallback menu.")

# =====================================================
# 🗄️ DATABASE (SQLite)
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "fruitbid.db")
from db import  *

init_db()

# =====================================================
# 🏠 APP MAIN
# =====================================================
page = render_sidebar()

if page == "🏠 Home":
    st.title("🍎 Welcome to FruitBid!")
    st.write("Buy and sell fresh fruits in real time 🍇🍉🍌")

elif page == "🏪 Marketplace":
    st.header("🍉 Marketplace")
    st.write("Live fruit lots will appear here.")

elif page == "💼 My Bids":
    st.header("💼 My Bids")
    st.write("Track your bids here.")

elif page == "⚙️ Add Lot (Admin)":
    st.header("⚙️ Add New Fruit Lot")
    fruit = st.text_input("Fruit name")
    price = st.number_input("Starting price", min_value=0.0, step=0.5)
    if st.button("Add Lot"):
        st.success(f"✅ {fruit} added with starting price ₹{price}")

# =====================================================
# ✅ FOOTER
# =====================================================
st.markdown("---")
st.caption("🍏 FruitBid App — powered by Streamlit & Supabase")
