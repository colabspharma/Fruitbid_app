# =====================================================
# 🏪 FruitBid Marketplace Page
# =====================================================

import streamlit as st
import sqlite3

# =====================================================
# ⚙️ Session State Initialization
# =====================================================
if "user_name" not in st.session_state:
    st.session_state.user_name = "Guest"
if "phone" not in st.session_state:
    st.session_state.phone = "N/A"
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

# =====================================================
# 📂 Imports & Setup
# =====================================================
try:
    from components.sidebar import render_sidebar
except ModuleNotFoundError:
    st.warning("⚠️ Sidebar component missing. Ensure `components/sidebar.py` exists.")
    
    def render_sidebar(_=None):
        """Fallback sidebar if component not found."""
        st.sidebar.title("Navigation")
        st.sidebar.write("🏠 Home")
        return None

DB_PATH = "fruitbid.db"

# =====================================================
# 🔒 Developer Login (temporary bypass)
# =====================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True
    st.session_state.user_name = "Developer"
    st.session_state.phone = "9999999999"

# =====================================================
# 🧭 Sidebar
# =====================================================
selected_page = render_sidebar("marketplace")

# =====================================================
# 🌟 Page Header
# =====================================================
st.title("🏪 Fruit Marketplace")
st.write(f"Welcome, **{st.session_state.user_name} ({st.session_state.phone})** 👋")
st.markdown("---")

# =====================================================
# 🧺 Fetch Lots from Database
# =====================================================
def fetch_lots():
    """Retrieve all available fruit lots from the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            # ✅ match actual database columns
            c.execute("""
                SELECT fruit_name, quantity_kg, base_price
                FROM lots ORDER BY id DESC
            """)
            return c.fetchall()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return []

# =====================================================
# 📦 Display Available Lots
# =====================================================

def fetch_lots():
    """Retrieve all available fruit lots from the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                SELECT item_name, quantity, base_price, date_added
                FROM lots ORDER BY id DESC
            """)
            return c.fetchall()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return []


# =====================================================
# 📦 Show Lots in UI
# =====================================================
lots = fetch_lots()

if lots:
    st.subheader("📦 Available Fruit Lots")

    for idx, (fruit, quantity, base_price, date_added) in enumerate(lots, start=1):
        with st.container():
            st.markdown(f"### 🍎 {fruit}")
            st.write(f"📦 **Quantity:** {quantity} kg")
            st.write(f"💰 **Base Price:** ₹{base_price}/kg")
            st.write(f"📅 **Date Added:** {date_added}")

            # Placeholder for bidding action
            st.button(f"💰 Place Bid on {fruit}", key=f"bid_{idx}")
            st.markdown("---")
else:
    st.info("No fruit lots available yet. Please add some from the ⚙️ Admin Add Lot page.")

# =====================================================
# 📦 Seed Sample Data (Auto-populate)
# =====================================================
def seed_sample_lots():
    """Insert a few fruit lots if the database is empty."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM lots")
            count = c.fetchone()[0]
            if count == 0:
                sample_data = [
                    ("Apples", 100, 120.0, "2025-10-08"),
                    ("Bananas", 200, 40.0, "2025-10-08"),
                    ("Mangoes", 150, 90.0, "2025-10-08"),
                    ("Oranges", 180, 75.0, "2025-10-08"),
                    ("Grapes", 250, 110.0, "2025-10-08")
                ]
                c.executemany(
                    "INSERT INTO lots (item_name, quantity, base_price, date_added) VALUES (?, ?, ?, ?)",
                    sample_data
                )
                conn.commit()
                st.success("🍉 Sample fruit lots added automatically!")
    except sqlite3.Error as e:
        st.error(f"Error populating sample lots: {e}")


# =====================================================
# 📦 Fetch Lots
# =====================================================
def fetch_lots():
    """Retrieve all available fruit lots from the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                SELECT item_name, quantity, base_price, date_added
                FROM lots ORDER BY id DESC
            """)
            return c.fetchall()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return []


# =====================================================
# 📦 Show Lots in UI
# =====================================================
seed_sample_lots()
lots = fetch_lots()
import time
if lots:
    st.subheader("📦 Available Fruit Lots")

    for idx, (fruit, quantity, base_price, date_added) in enumerate(lots, start=1):
        with st.container():
            st.markdown(f"### 🍎 {fruit}")
            st.write(f"📦 **Quantity:** {quantity} kg")
            st.write(f"💰 **Base Price:** ₹{base_price}/kg")
            st.write(f"📅 **Date Added:** {date_added}")
            st.button(f"💰 Place Bid on {fruit}", key=f"bid_{idx}_{int(time.time())}")
            st.markdown("---")
            
else:
    st.info("No fruit lots available yet. Please add some from the ⚙️ Admin Add Lot page.")

# =====================================================
# 🧾 Footer Note
# =====================================================
st.caption("💡 All lots shown here are fetched live from `fruitbid.db`.")
