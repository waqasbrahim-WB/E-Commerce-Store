import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="My Own Store", page_icon="🛍️", layout="wide")

# --- CUSTOM CSS FOR IMAGES ---
st.markdown("""
<style>
    .product-card {
        padding: 1rem;
        border-radius: 15px;
        background-color: white;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
        text-align: center;
    }
    .stImage > img {
        border-radius: 10px;
        height: 200px;
        object-fit: cover;
    }
    .price-text { color: #1e88e5; font-weight: bold; font-size: 1.3rem; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'wishlist' not in st.session_state: st.session_state.wishlist = []

# --- PRODUCT DATA (Apni Images Yahan Add Karein) ---
# Note: Agar images 'assets' folder mein hain toh path aise hoga: "assets/image_name.jpg"
products = [
    {"id": 1, "name": "Ultra Pods", "price": 199, "img": "https://via.placeholder.com/300", "cat": "Electronics"},
    {"id": 2, "name": "Smart Watch", "price": 250, "img": "https://via.placeholder.com/300", "cat": "Electronics"},
    {"id": 3, "name": "Mechanical KB", "price": 120, "img": "https://via.placeholder.com/300", "cat": "Electronics"},
    {"id": 4, "name": "Travel Bag", "price": 50, "img": "https://via.placeholder.com/300", "cat": "Fashion"},
    {"id": 5, "name": "Sneakers", "price": 90, "img": "https://via.placeholder.com/300", "cat": "Fashion"},
    {"id": 6, "name": "Wallet", "price": 30, "img": "https://via.placeholder.com/300", "cat": "Fashion"},
    {"id": 7, "name": "Coffee", "price": 15, "img": "https://via.placeholder.com/300", "cat": "Food"},
    {"id": 8, "name": "Bottle", "price": 20, "img": "https://via.placeholder.com/300", "cat": "Food"},
]

# --- UI LAYOUT ---
st.title("🛒 Mera E-Commerce Store")

# Sidebar for Cart
with st.sidebar:
    st.header("Aapka Cart")
    total = 0
    for p_id, qty in list(st.session_state.cart.items()):
        p = next(x for x in products if x["id"] == p_id)
        st.write(f"**{p['name']}** (x{qty})")
        total += p['price'] * qty
    st.divider()
    st.subheader(f"Total: ${total}")
    if st.button("Checkout"):
        st.success("Order Successful!")
        st.session_state.cart = {}
        st.rerun()

# Category Filter
cat = st.tabs(["All Products", "Electronics", "Fashion", "Food"])

# Main Grid
cols = st.columns(4)
for idx, p in enumerate(products):
    with cols[idx % 4]:
        with st.container():
            st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
            # YAHAN IMAGE DISPLAY HOTI HAI
            # Agar aapne local file use karni hai toh p['img'] mein path dein
            st.image(p['img'], use_container_width=True)
            st.subheader(p['name'])
            st.markdown(f'<p class="price-text">${p["price"]}</p>', unsafe_allow_html=True)
            
            if st.button(f"Add to Cart", key=f"btn_{p['id']}"):
                st.session_state.cart[p['id']] = st.session_state.cart.get(p['id'], 0) + 1
                st.toast(f"{p['name']} added!")
            st.markdown('</div>', unsafe_allow_html=True)
