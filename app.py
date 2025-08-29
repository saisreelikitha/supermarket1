import streamlit as st
import pandas as pd

st.set_page_config(page_title="Supermarket Daily Sales", layout="centered")

st.title("🛒 Supermarket Daily Sales Tracker")

# initialize session state
if "sales" not in st.session_state:
    st.session_state["sales"] = []

with st.form("sales_entry"):
    st.subheader("Enter Today's Sales")
    product = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    price = st.number_input("Price per unit", min_value=0.0, step=0.1, format="%.2f")
    submitted = st.form_submit_button("Add Sale")

    if submitted:
        if not product:
            st.error("Please enter a product name.")
        else:
            revenue = quantity * price
            st.session_state["sales"].append({
                "Product": product.strip(),
                "Quantity": int(quantity),
                "Price": float(price),
                "Revenue": float(revenue)
            })
            st.success(f"Added: {product} — Revenue: ₹{revenue:.2f}")

if st.session_state["sales"]:
    df = pd.DataFrame(st.session_state["sales"])
    st.subheader("📊 Sales Data")
    st.dataframe(df, use_container_width=True)

    total_revenue = df["Revenue"].sum()
    st.metric("💰 Total Revenue (Today)", f"₹{total_revenue:.2f}")

    st.subheader("📈 Product Revenue Analysis")
    chart_data = df.groupby("Product")["Revenue"].sum().reset_index()
    st.bar_chart(chart_data.set_index("Product"))
else:
    st.info("No sales recorded yet. Use the form above to add sales.")
