import streamlit as st

# Page config
st.set_page_config(page_title="🛒 E-Commerce Store", layout="wide")

# Sample product catalog
products = [
    {"id": 1, "name": "Laptop", "price": 800, "image": "💻"},
    {"id": 2, "name": "Smartphone", "price": 500, "image": "📱"},
    {"id": 3, "name": "Headphones", "price": 150, "image": "🎧"},
    {"id": 4, "name": "Smartwatch", "price": 200, "image": "⌚"},
    {"id": 5, "name": "Camera", "price": 600, "image": "📷"},
]

# Initialize cart in session state
if "cart" not in st.session_state:
    st.session_state.cart = []

st.title("🛒 E-Commerce Store")
st.write("Browse products and add them to your cart!")

# Display products in columns
cols = st.columns(3)
for i, product in enumerate(products):
    with cols[i % 3]:
        st.markdown(f"### {product['image']} {product['name']}")
        st.markdown(f"💲 **Price:** ${product['price']}")
        if st.button(f"Add to Cart - {product['name']}", key=product["id"]):
            st.session_state.cart.append(product)
            st.success(f"{product['name']} added to cart!")

# Cart Section
st.markdown("---")
st.header("🛍️ Your Cart")

if st.session_state.cart:
    total = sum(item["price"] for item in st.session_state.cart)
    for item in st.session_state.cart:
        st.write(f"- {item['image']} {item['name']} - ${item['price']}")
    st.markdown(f"### 💵 Total: ${total}")
    if st.button("Checkout"):
        st.success("✅ Order placed successfully! Thank you for shopping.")
        st.session_state.cart = []  # Clear cart after checkout
else:
    st.info("Your cart is empty. Add some products!")
