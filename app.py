"""
E-Commerce Store - Streamlit App
A modern, responsive e-commerce application with shopping cart functionality.
"""

import streamlit as st
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="StyleCart - Your Fashion Destination",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        font-size: 3rem;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Product cards */
    .product-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.3s, box-shadow 0.3s;
        height: 100%;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    
    .product-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0.5rem 0;
        color: #333;
    }
    
    .product-price {
        font-size: 1.5rem;
        font-weight: 700;
        color: #FF6B6B;
        margin: 0.5rem 0;
    }
    
    .product-category {
        display: inline-block;
        background: #f0f0f0;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        color: #666;
        margin: 0.3rem 0;
    }
    
    /* Buttons */
    .stButton button {
        width: 100%;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .add-to-cart-btn {
        background: linear-gradient(45deg, #4ECDC4, #44A08D);
        color: white;
    }
    
    .add-to-cart-btn:hover {
        background: linear-gradient(45deg, #44A08D, #4ECDC4);
        transform: scale(1.05);
    }
    
    .checkout-btn {
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
    }
    
    .remove-btn {
        background: #ffebee;
        color: #c62828;
        border: 1px solid #ffcdd2 !important;
    }
    
    /* Cart styling */
    .cart-item {
        padding: 0.8rem;
        border-bottom: 1px solid #eee;
    }
    
    .cart-total {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #4ECDC4;
    }
    
    /* Badge for cart count */
    .cart-badge {
        background: #FF6B6B;
        color: white;
        border-radius: 50%;
        padding: 0.2rem 0.6rem;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    
    /* Sale badge */
    .sale-badge {
        background: #FF6B6B;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 4px;
        font-size: 0.8rem;
        position: absolute;
        top: 10px;
        right: 10px;
    }
    
    /* Rating stars */
    .rating {
        color: #FFD700;
        font-size: 1rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        .product-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'wishlist' not in st.session_state:
    st.session_state.wishlist = set()

# Product Data
PRODUCTS = [
    {
        "id": 1,
        "name": "Classic White Sneakers",
        "price": 79.99,
        "category": "Footwear",
        "emoji": "👟",
        "description": "Comfortable, versatile white sneakers for everyday wear",
        "rating": 4.5,
        "stock": 15,
        "image_color": "#F5F5F5",
        "on_sale": True,
        "original_price": 99.99
    },
    {
        "id": 2,
        "name": "Wireless Bluetooth Headphones",
        "price": 129.99,
        "category": "Electronics",
        "emoji": "🎧",
        "description": "Noise-cancelling headphones with 30-hour battery",
        "rating": 4.8,
        "stock": 8,
        "image_color": "#2C3E50",
        "on_sale": False
    },
    {
        "id": 3,
        "name": "Organic Cotton T-Shirt",
        "price": 24.99,
        "category": "Clothing",
        "emoji": "👕",
        "description": "Soft, sustainable cotton t-shirt in multiple colors",
        "rating": 4.3,
        "stock": 25,
        "image_color": "#3498DB",
        "on_sale": True,
        "original_price": 34.99
    },
    {
        "id": 4,
        "name": "Smart Watch Series 5",
        "price": 299.99,
        "category": "Electronics",
        "emoji": "⌚",
        "description": "Fitness tracking, heart rate monitor, GPS",
        "rating": 4.7,
        "stock": 5,
        "image_color": "#1ABC9C",
        "on_sale": False
    },
    {
        "id": 5,
        "name": "Leather Backpack",
        "price": 89.99,
        "category": "Accessories",
        "emoji": "🎒",
        "description": "Genuine leather backpack with laptop compartment",
        "rating": 4.6,
        "stock": 12,
        "image_color": "#8B4513",
        "on_sale": True,
        "original_price": 119.99
    },
    {
        "id": 6,
        "name": "Yoga Mat Premium",
        "price": 39.99,
        "category": "Fitness",
        "emoji": "🧘",
        "description": "Non-slip, eco-friendly yoga mat with carrying strap",
        "rating": 4.4,
        "stock": 20,
        "image_color": "#27AE60",
        "on_sale": False
    },
    {
        "id": 7,
        "name": "Ceramic Coffee Mug",
        "price": 16.99,
        "category": "Home",
        "emoji": "☕",
        "description": "Handcrafted ceramic mug with insulated design",
        "rating": 4.2,
        "stock": 30,
        "image_color": "#E74C3C",
        "on_sale": True,
        "original_price": 22.99
    },
    {
        "id": 8,
        "name": "Gaming Mouse Pro",
        "price": 59.99,
        "category": "Electronics",
        "emoji": "🖱️",
        "description": "RGB gaming mouse with customizable buttons",
        "rating": 4.9,
        "stock": 7,
        "image_color": "#9B59B6",
        "on_sale": False
    }
]

# Helper Functions
def add_to_cart(product_id, quantity=1):
    """Add product to cart"""
    if product_id in st.session_state.cart:
        st.session_state.cart[product_id] += quantity
    else:
        st.session_state.cart[product_id] = quantity
    st.success(f"Added to cart! 🛒")
    st.rerun()

def remove_from_cart(product_id):
    """Remove product from cart"""
    if product_id in st.session_state.cart:
        del st.session_state.cart[product_id]
        st.success("Item removed from cart")
        st.rerun()

def clear_cart():
    """Clear all items from cart"""
    st.session_state.cart.clear()
    st.success("Cart cleared!")

def checkout():
    """Process checkout"""
    if not st.session_state.cart:
        st.warning("Your cart is empty!")
        return
    
    total = calculate_cart_total()
    order = {
        "timestamp": datetime.now(),
        "items": st.session_state.cart.copy(),
        "total": total,
        "order_id": f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    }
    
    st.session_state.orders.append(order)
    st.session_state.cart.clear()
    
    # Show success message
    st.balloons()
    st.success(f"""
    🎉 Order Successful!
    
    **Order ID:** {order['order_id']}
    **Total:** ${total:.2f}
    **Items:** {sum(st.session_state.cart.values())}
    
    Thank you for your purchase! Your items will be shipped soon.
    """)

def calculate_cart_total():
    """Calculate total cart value"""
    total = 0
    for product_id, quantity in st.session_state.cart.items():
        product = next((p for p in PRODUCTS if p["id"] == product_id), None)
        if product:
            total += product["price"] * quantity
    return total

def get_cart_count():
    """Get total number of items in cart"""
    return sum(st.session_state.cart.values())

def get_product_by_id(product_id):
    """Get product by ID"""
    return next((p for p in PRODUCTS if p["id"] == product_id), None)

# UI Components
def display_header():
    """Display main header"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-header">🛍️ StyleCart</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Discover premium products with seamless shopping experience</p>', unsafe_allow_html=True)

def display_product_card(product):
    """Display individual product card"""
    with st.container():
        # Product card container
        st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
        
        # Sale badge
        if product.get("on_sale", False):
            st.markdown(f'<div class="sale-badge">SALE</div>', unsafe_allow_html=True)
        
        # Product emoji/icon
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f'<div style="font-size: 2.5rem; text-align: center;">{product["emoji"]}</div>', unsafe_allow_html=True)
        
        with col2:
            # Product info
            st.markdown(f'<div class="product-title">{product["name"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="product-category">{product["category"]}</div>', unsafe_allow_html=True)
            
            # Rating
            stars = "★" * int(product["rating"]) + "☆" * (5 - int(product["rating"]))
            st.markdown(f'<div class="rating">{stars} ({product["rating"]})</div>', unsafe_allow_html=True)
            
            # Price
            if product.get("on_sale", False):
                st.markdown(f'''
                <div>
                    <span class="product-price">${product["price"]:.2f}</span>
                    <span style="text-decoration: line-through; color: #999; margin-left: 10px;">
                        ${product["original_price"]:.2f}
                    </span>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="product-price">${product["price"]:.2f}</div>', unsafe_allow_html=True)
            
            # Stock indicator
            stock_color = "#2ECC71" if product["stock"] > 10 else "#E74C3C" if product["stock"] > 0 else "#95A5A6"
            stock_text = f"In Stock ({product['stock']})" if product["stock"] > 0 else "Out of Stock"
            st.markdown(f'<div style="color: {stock_color}; font-size: 0.9rem; margin: 5px 0;">{stock_text}</div>', unsafe_allow_html=True)
        
        # Add to cart button
        col1, col2 = st.columns(2)
        with col1:
            quantity = st.number_input(
                "Qty", 
                min_value=1, 
                max_value=min(10, product["stock"]), 
                value=1,
                key=f"qty_{product['id']}",
                label_visibility="collapsed"
            )
        
        with col2:
            if product["stock"] > 0:
                if st.button(
                    "Add to Cart",
                    key=f"add_{product['id']}",
                    use_container_width=True,
                    type="secondary"
                ):
                    add_to_cart(product["id"], quantity)
            else:
                st.button(
                    "Out of Stock",
                    disabled=True,
                    use_container_width=True
                )
        
        # Product description (collapsed by default)
        with st.expander("📋 Details"):
            st.write(product["description"])
            st.caption(f"Product ID: {product['id']}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def display_sidebar():
    """Display shopping cart sidebar"""
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center;'>
            <h2>🛒 Your Cart <span class='cart-badge'>{get_cart_count()}</span></h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Free shipping progress
        cart_total = calculate_cart_total()
        free_shipping_threshold = 100
        progress = min(cart_total / free_shipping_threshold, 1)
        
        if cart_total < free_shipping_threshold:
            st.progress(progress)
            st.caption(f"🎁 Add ${free_shipping_threshold - cart_total:.2f} more for free shipping!")
        else:
            st.success("🎉 You've earned free shipping!")
        
        st.divider()
        
        # Cart items
        if not st.session_state.cart:
            st.info("Your cart is empty")
            st.markdown("---")
            st.markdown("### 🎯 Hot Deals")
            st.write("• Add $100+ for free shipping")
            st.write("• Use code: STYLE10 for 10% off")
            st.write("• New customer? Get 15% off!")
        else:
            for product_id, quantity in st.session_state.cart.items():
                product = get_product_by_id(product_id)
                if product:
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.write(f"{product['emoji']} {product['name']}")
                    with col2:
                        st.write(f"${product['price']} × {quantity}")
                    with col3:
                        if st.button("❌", key=f"remove_{product_id}"):
                            remove_from_cart(product_id)
            
            st.divider()
            
            # Cart summary
            subtotal = calculate_cart_total()
            shipping = 0 if subtotal >= 100 else 9.99
            tax = subtotal * 0.08
            total = subtotal + shipping + tax
            
            st.markdown(f"""
            <div class='cart-total'>
                <h4>Order Summary</h4>
                <p>Subtotal: <strong>${subtotal:.2f}</strong></p>
                <p>Shipping: <strong>${shipping:.2f}</strong></p>
                <p>Tax (8%): <strong>${tax:.2f}</strong></p>
                <hr>
                <h3>Total: ${total:.2f}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Checkout buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Clear Cart", use_container_width=True, type="secondary"):
                    clear_cart()
            with col2:
                if st.button("Checkout Now", use_container_width=True, type="primary"):
                    checkout()
        
        # Order history
        if st.session_state.orders:
            st.divider()
            with st.expander("📋 Order History"):
                for order in st.session_state.orders[-3:]:  # Show last 3 orders
                    st.write(f"**{order['order_id']}**")
                    st.write(f"${order['total']:.2f} • {order['timestamp'].strftime('%b %d, %H:%M')}")
                    st.caption(f"{len(order['items'])} items")

def display_products_grid():
    """Display products in a responsive grid"""
    # Filters and sorting
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        categories = ["All"] + list(set(p["category"] for p in PRODUCTS))
        selected_category = st.selectbox("Filter by Category", categories)
    
    with col2:
        sort_options = ["Featured", "Price: Low to High", "Price: High to Low", "Name"]
        sort_by = st.selectbox("Sort by", sort_options)
    
    with col3:
        price_range = st.slider("Price Range", 0, 300, (0, 300))
    
    # Filter products
    filtered_products = PRODUCTS.copy()
    
    if selected_category != "All":
        filtered_products = [p for p in filtered_products if p["category"] == selected_category]
    
    filtered_products = [p for p in filtered_products if price_range[0] <= p["price"] <= price_range[1]]
    
    # Sort products
    if sort_by == "Price: Low to High":
        filtered_products.sort(key=lambda x: x["price"])
    elif sort_by == "Price: High to Low":
        filtered_products.sort(key=lambda x: x["price"], reverse=True)
    elif sort_by == "Name":
        filtered_products.sort(key=lambda x: x["name"])
    
    # Display products in grid
    st.markdown(f"### 📦 Products ({len(filtered_products)})")
    
    # Responsive grid: 4 columns on desktop, 2 on mobile
    cols = st.columns(4)
    
    for idx, product in enumerate(filtered_products):
        with cols[idx % 4]:
            display_product_card(product)

def display_footer():
    """Display app footer"""
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🛍️ StyleCart")
        st.caption("Premium online shopping experience")
    
    with col2:
        st.markdown("### 🔒 Secure Shopping")
        st.caption("• SSL Encrypted")
        st.caption("• Privacy Protected")
        st.caption("• Money Back Guarantee")
    
    with col3:
        st.markdown("### 📞 Contact")
        st.caption("support@stylecart.com")
        st.caption("+1 (555) 123-4567")
    
    st.markdown("---")
    st.caption("© 2024 StyleCart. All rights reserved. | This is a demo e-commerce application.")

# Main App
def main():
    """Main app function"""
    display_header()
    display_sidebar()
    display_products_grid()
    
    # Featured products section
    st.markdown("---")
    st.markdown("## ⭐ Featured Products")
    featured_cols = st.columns(4)
    featured_products = [p for p in PRODUCTS if p.get("on_sale", False) or p["rating"] >= 4.7]
    
    for idx, product in enumerate(featured_products[:4]):
        with featured_cols[idx]:
            display_product_card(product)
    
    display_footer()

if __name__ == "__main__":
    main()
