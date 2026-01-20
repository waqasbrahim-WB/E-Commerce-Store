import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Zenith E-Commerce", page_icon="🛍️", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Global Styles */
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    
    /* Product Card Styling */
    .product-card {
        padding: 1.5rem;
        border-radius: 12px;
        background-color: white;
        border: 1px solid #eee;
        margin-bottom: 1rem;
        height: 100%;
    }
    .price-tag { color: #2e7d32; font-weight: bold; font-size: 1.2rem; }
    .sale-tag { color: #d32f2f; font-weight: bold; font-size: 0.9rem; }
    
    /* Sidebar Styling */
    .css-1d391kg { background-color: white; }
    
    /* Metric Styling */
    [data-testid="stMetricValue"] { font-size: 1.5rem; color: #1565c0; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'wishlist' not in st.session_state:
    st.session_state.wishlist = []
if 'orders' not in st.session_state:
    st.session_state.orders = []

# --- SAMPLE DATA ---
products = [
    {"id": 1, "name": "Ultra-Pods Pro", "price": 199.99, "category": "Electronics", "icon": "🎧", "desc": "Noise-cancelling wireless earbuds.", "stock": 15, "rating": 4.8, "sale": True},
    {"id": 2, "name": "Smart Watch G3", "price": 249.00, "category": "Electronics", "icon": "⌚", "desc": "Track your fitness and heart rate.", "stock": 8, "rating": 4.5, "sale": False},
    {"id": 3, "name": "Mechanical Keyboard", "price": 120.00, "category": "Electronics", "icon": "⌨️", "desc": "RGB tactile typing experience.", "stock": 20, "rating": 4.9, "sale": False},
    {"id": 4, "name": "Canvas Backpack", "price": 55.00, "category": "Fashion", "icon": "🎒", "desc": "Durable and stylish for travel.", "stock": 25, "rating": 4.2, "sale": True},
    {"id": 5, "name": "Performance Sneakers", "price": 89.00, "category": "Fashion", "icon": "👟", "desc": "Lightweight running shoes.", "stock": 12, "rating": 4.6, "sale": False},
    {"id": 6, "name": "Leather Wallet", "price": 45.00, "category": "Fashion", "icon": "👛", "desc": "Genuine handcrafted leather.", "stock": 30, "rating": 4.7, "sale": False},
    {"id": 7, "name": "Organic Coffee Beans", "price": 18.50, "category": "Groceries", "icon": "☕", "desc": "Ethically sourced dark roast.", "stock": 50, "rating": 5.0, "sale": True},
    {"id": 8, "name": "Glass Water Bottle", "price": 22.00, "category": "Groceries", "icon": "🍶", "desc": "Eco-friendly 1L bottle.", "stock": 40, "rating": 4.3, "sale": False},
]

# --- HELPER FUNCTIONS ---
def add_to_cart(p_id):
    st.session_state.cart[p_id] = st.session_state.cart.get(p_id, 0) + 1
    st.toast(f"Added to cart! 🛒")

def remove_from_cart(p_id):
    if p_id in st.session_state.cart:
        del st.session_state.cart[p_id]
        st.toast("Removed from cart.", icon="🗑️")

def toggle_wishlist(p_id):
    if p_id in st.session_state.wishlist:
        st.session_state.wishlist.remove(p_id)
    else:
        st.session_state.wishlist.append(p_id)

# --- SIDEBAR: CART & NAVIGATION ---
with st.sidebar:
    st.title("🛒 Your Basket")
    
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        total_cost = 0
        for p_id, qty in list(st.session_state.cart.items()):
            p = next(item for item in products if item["id"] == p_id)
            subtotal = p["price"] * qty
            total_cost += subtotal
            
            col1, col2 = st.columns([3, 1])
            col1.write(f"**{p['icon']} {p['name']}** \n{qty} x ${p['price']}")
            if col2.button("❌", key=f"del_{p_id}"):
                remove_from_cart(p_id)
                st.rerun()
        
        st.divider()
        st.metric("Total", f"${total_cost:.2f}")
        
        # Free Shipping Progress
        shipping_threshold = 200
        progress = min(total_cost / shipping_threshold, 1.0)
        st.write(f"🚚 Free shipping at ${shipping_threshold}")
        st.progress(progress)
        if total_cost < shipping_threshold:
            st.caption(f"Add **${shipping_threshold - total_cost:.2f}** more for free shipping!")
        else:
            st.success("You unlocked free shipping!")

        if st.button("Proceed to Checkout", type="primary"):
            # Mock Checkout Logic
            order_id = f"ORD-{datetime.now().strftime('%M%S')}"
            st.session_state.orders.append({"id": order_id, "total": total_cost, "date": datetime.now()})
            st.session_state.cart = {}
            st.success(f"Order {order_id} placed successfully!")
            st.balloons()
            st.rerun()

# --- MAIN UI ---
st.title("🛍️ Zenith E-Commerce")
st.markdown("---")

# Filters & Search
c1, c2, c3 = st.columns([2, 1, 1])
search_query = c1.text_input("Search products...", placeholder="I'm looking for...")
category_filter = c2.selectbox("Category", ["All", "Electronics", "Fashion", "Groceries"])
sort_option = c3.selectbox("Sort by", ["Name", "Price: Low to High", "Price: High to Low", "Rating"])

# Filter Logic
filtered_products = [p for p in products if search_query.lower() in p["name"].lower()]
if category_filter != "All":
    filtered_products = [p for p in filtered_products if p["category"] == category_filter]

# Sorting Logic
if sort_option == "Price: Low to High":
    filtered_products.sort(key=lambda x: x["price"])
elif sort_option == "Price: High to Low":
    filtered_products.sort(key=lambda x: x["price"], reverse=True)
elif sort_option == "Rating":
    filtered_products.sort(key=lambda x: x["rating"], reverse=True)
else:
    filtered_products.sort(key=lambda x: x["name"])

# --- PRODUCT GRID ---
if not filtered_products:
    st.warning("No products found. Try adjusting your filters.")
else:
    # Creating a 4-column responsive grid
    cols = st.columns(4)
    for idx, p in enumerate(filtered_products):
        with cols[idx % 4]:
            with st.container():
                st.markdown(f"""
                <div class="product-card">
                    <h1 style="font-size: 3rem; margin: 0;">{p['icon']}</h1>
                    <h3>{p['name']}</h3>
                    <p style="font-size: 0.8rem; color: #666;">{p['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Metadata row
                m1, m2 = st.columns(2)
                price_label = f"${p['price']}"
                if p['sale']:
                    m1.markdown(f"<span class='sale-tag'>SALE</span> <br> <span class='price-tag'>{price_label}</span>", unsafe_allow_html=True)
                else:
                    m1.markdown(f"<span class='price-tag'>{price_label}</span>", unsafe_allow_html=True)
                
                m2.markdown(f"⭐ {p['rating']}")
                
                # Stock & Actions
                st.caption(f"In stock: {p['stock']}")
                
                # Interaction Buttons
                ca1, ca2 = st.columns([3, 1])
                if ca1.button("Add to Cart", key=f"add_{p['id']}", type="secondary"):
                    add_to_cart(p['id'])
                
                heart_icon = "❤️" if p['id'] in st.session_state.wishlist else "🤍"
                if ca2.button(heart_icon, key=f"wish_{p['id']}"):
                    toggle_wishlist(p['id'])
                    st.rerun()

                with st.expander("Details"):
                    st.write(f"**Category:** {p['category']}")
                    st.write(p['desc'])
                    st.info("💡 Standard 2-year warranty applies to this item.")

# --- FOOTER / ORDER HISTORY ---
st.markdown("---")
with st.expander("📜 Order History"):
    if not st.session_state.orders:
        st.write("No orders yet.")
    else:
        history_df = pd.DataFrame(st.session_state.orders)
        st.dataframe(history_df, use_container_width=True)

if st.session_state.wishlist:
    st.markdown("### ✨ Your Wishlist")
    w_cols = st.columns(len(st.session_state.wishlist) if len(st.session_state.wishlist) < 6 else 6)
    for i, w_id in enumerate(st.session_state.wishlist):
        wp = next(item for item in products if item["id"] == w_id)
        with w_cols[i % 6]:
            st.button(f"{wp['icon']} {wp['name']}", key=f"w_btn_{w_id}")
