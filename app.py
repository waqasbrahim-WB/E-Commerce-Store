import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="SwiftShop | E-Commerce Store", page_icon="🛍️", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; transition: all 0.3s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .product-card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        border: 1px solid #eee;
        margin-bottom: 20px;
    }
    .price-tag { color: #2e7d32; font-weight: bold; font-size: 1.2rem; }
    .discount-tag { color: #d32f2f; font-size: 0.8rem; text-decoration: line-through; }
    .cart-badge {
        background-color: #ff4b4b;
        color: white;
        padding: 2px 8px;
        border-radius: 50%;
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'wishlist' not in st.session_state:
    st.session_state.wishlist = []
if 'orders' not in st.session_state:
    st.session_state.orders = []

# --- SAMPLE DATA ---
products = [
    {"id": 1, "name": "Ultra-Pods Pro", "price": 199.99, "category": "Electronics", "emoji": "🎧", "stock": 15, "rating": 4.8, "old_price": 249.99, "desc": "Noise-cancelling wireless earbuds."},
    {"id": 2, "name": "Smart Watch Series 9", "price": 399.00, "category": "Electronics", "emoji": "⌚", "stock": 8, "rating": 4.9, "old_price": None, "desc": "Health tracking at your wrist."},
    {"id": 3, "name": "Cotton Crew Tee", "price": 25.00, "category": "Apparel", "emoji": "👕", "stock": 50, "rating": 4.2, "old_price": 35.00, "desc": "100% organic cotton comfort."},
    {"id": 4, "name": "Leather Messenger Bag", "price": 120.00, "category": "Accessories", "emoji": "💼", "stock": 5, "rating": 4.5, "old_price": 150.00, "desc": "Handcrafted genuine leather."},
    {"id": 5, "name": "Mechanical Keyboard", "price": 89.99, "category": "Electronics", "emoji": "⌨️", "stock": 12, "rating": 4.7, "old_price": None, "desc": "RGB backlit tactile switches."},
    {"id": 6, "name": "Running Sneakers", "price": 75.00, "category": "Apparel", "emoji": "👟", "stock": 20, "rating": 4.4, "old_price": 95.00, "desc": "Lightweight breathable mesh."},
    {"id": 7, "name": "Minimalist Wallet", "price": 45.00, "category": "Accessories", "emoji": "👛", "stock": 30, "rating": 4.6, "old_price": None, "desc": "RFID blocking slim design."},
    {"id": 8, "name": "Pro Gaming Mouse", "price": 59.00, "category": "Electronics", "emoji": "🖱️", "stock": 0, "rating": 4.3, "old_price": 79.00, "desc": "25k DPI optical sensor."}
]

# --- HELPER FUNCTIONS ---
def add_to_cart(product_id, qty):
    if str(product_id) in st.session_state.cart:
        st.session_state.cart[str(product_id)] += qty
    else:
        st.session_state.cart[str(product_id)] = qty
    st.toast(f"Added to cart! 🛒")

def toggle_wishlist(product_id):
    if product_id in st.session_state.wishlist:
        st.session_state.wishlist.remove(product_id)
        st.toast("Removed from wishlist")
    else:
        st.session_state.wishlist.append(product_id)
        st.toast("Added to wishlist! ❤️")

# --- SIDEBAR (Cart & Filters) ---
with st.sidebar:
    st.title("🛒 Your Cart")
    cart_total = 0
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        for p_id, qty in list(st.session_state.cart.items()):
            p = next(item for item in products if str(item["id"]) == p_id)
            subtotal = p["price"] * qty
            cart_total += subtotal
            col1, col2 = st.columns([3, 1])
            col1.write(f"**{p['emoji']} {p['name']}** \n{qty} x ${p['price']}")
            if col2.button("❌", key=f"del_{p_id}"):
                del st.session_state.cart[p_id]
                st.rerun()
        
        st.divider()
        st.write(f"### Total: ${cart_total:.2f}")
        
        # Free Shipping Progress Bar
        threshold = 500
        progress = min(cart_total / threshold, 1.0)
        st.write(f"🚚 Free Shipping Threshold ($500)")
        st.progress(progress)
        if cart_total < threshold:
            st.caption(f"Add ${threshold - cart_total:.2f} more for free shipping!")
        else:
            st.success("You qualify for FREE shipping!")

        if st.button("Proceed to Checkout", type="primary", use_container_width=True):
            order = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": cart_total, "items": len(st.session_state.cart)}
            st.session_state.orders.append(order)
            st.session_state.cart = {}
            st.balloons()
            st.success("Order Placed Successfully!")
            st.rerun()

# --- MAIN UI ---
st.title("SwiftShop")
st.markdown("#### Premium Quality. Fast Delivery.")

# Search and Filters
col_search, col_sort = st.columns([2, 1])
search_query = col_search.text_input("🔍 Search products...", placeholder="What are you looking for?")
sort_option = col_sort.selectbox("Sort by", ["Newest", "Price: Low to High", "Price: High to Low", "Rating"])

tab1, tab2, tab3, tab4 = st.tabs(["🛍️ Shop", "❤️ Wishlist", "📦 Orders", "ℹ️ About"])

with tab1:
    # Category Filter
    categories = ["All"] + list(set(p["category"] for p in products))
    selected_cat = st.segmented_control("Categories", categories, default="All")
    
    price_range = st.slider("Price Range ($)", 0, 500, (0, 500))

    # Filter Logic
    filtered_prods = [p for p in products if (selected_cat == "All" or p["category"] == selected_cat) 
                      and (search_query.lower() in p["name"].lower())
                      and (price_range[0] <= p["price"] <= price_range[1])]
    
    if sort_option == "Price: Low to High":
        filtered_prods.sort(key=lambda x: x["price"])
    elif sort_option == "Price: High to Low":
        filtered_prods.sort(key=lambda x: x["price"], reverse=True)
    elif sort_option == "Rating":
        filtered_prods.sort(key=lambda x: x["rating"], reverse=True)

    # Product Grid
    if not filtered_prods:
        st.warning("No products found matching your criteria.")
    else:
        cols = st.columns(3)
        for idx, p in enumerate(filtered_prods):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="product-card">
                    <h1 style='text-align: center; margin: 0;'>{p['emoji']}</h1>
                    <h3>{p['name']}</h3>
                    <p style='color: gray; font-size: 0.9rem;'>{p['category']}</p>
                    <p>{p['desc']}</p>
                    <p>⭐ {p['rating']} | <span class='price-tag'>${p['price']}</span> 
                    {f"<span class='discount-tag'>${p['old_price']}</span>" if p['old_price'] else ""}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Availability logic
                if p['stock'] > 0:
                    st.caption(f"✅ In Stock ({p['stock']} units)")
                    qty = st.number_input("Qty", min_value=1, max_value=p['stock'], key=f"qty_{p['id']}", label_visibility="collapsed")
                    
                    c1, c2 = st.columns(2)
                    c1.button("Add 🛒", key=f"btn_{p['id']}", on_click=add_to_cart, args=(p['id'], qty))
                    wish_label = "❤️" if p['id'] in st.session_state.wishlist else "🤍"
                    c2.button(wish_label, key=f"wish_{p['id']}", on_click=toggle_wishlist, args=(p['id'],))
                else:
                    st.error("Out of Stock")
                
                with st.expander("View Details"):
                    st.write("Customer Reviews:")
                    st.caption("- 'Best purchase ever!' - ⭐⭐⭐⭐⭐")
                    st.caption("- 'Fast shipping and great quality.' - ⭐⭐⭐⭐")

with tab2:
    st.header("My Wishlist")
    wish_items = [p for p in products if p['id'] in st.session_state.wishlist]
    if not wish_items:
        st.info("Your wishlist is empty.")
    else:
        for wp in wish_items:
            st.write(f"{wp['emoji']} **{wp['name']}** - ${wp['price']}")

with tab3:
    st.header("Order History")
    if not st.session_state.orders:
        st.info("No orders yet. Start shopping!")
    else:
        df_orders = pd.DataFrame(st.session_state.orders)
        st.table(df_orders)

with tab4:
    st.header("About SwiftShop")
    st.write("This is a high-performance Streamlit E-Commerce template designed for speed and user experience.")
