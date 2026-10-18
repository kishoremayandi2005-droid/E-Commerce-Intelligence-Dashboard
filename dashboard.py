
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="E-Commerce Intelligence",
    page_icon="📊",
    layout="wide"
)

# Dashboard styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef4ff, #f8fbff);
}
h1, h2, h3 {
    color: #15345b;
}
[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #dce6f5;
    padding: 18px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 E-Commerce Intelligence Dashboard")
st.caption("Sales performance • Product insights • Customer segmentation")
st.info(
    "Portfolio project using the UCI Online Retail dataset. "
    "This is Amazon-inspired analytics, not actual Amazon company data."
)

# Load cleaned dataset
data_file = Path("cleaned_retail_data.csv")
if not data_file.exists():
    st.error("cleaned_retail_data.csv not found. Run analysis.py first.")
    st.stop()

df = pd.read_csv(data_file)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df = df.dropna(subset=["InvoiceDate", "Revenue"])

# Sidebar filters
st.sidebar.header("Dashboard Filters")

countries = sorted(df["Country"].dropna().unique().tolist())
selected_countries = st.sidebar.multiselect(
    "Select countries",
    countries,
    default=countries
)

min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

date_range = st.sidebar.date_input(
    "Invoice date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered = df[df["Country"].isin(selected_countries)].copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        (filtered["InvoiceDate"].dt.date >= start_date)
        & (filtered["InvoiceDate"].dt.date <= end_date)
    ]

if filtered.empty:
    st.warning("No transactions match these filters. Change your selections.")
    st.stop()

# KPI metrics
total_revenue = filtered["Revenue"].sum()
total_orders = filtered["InvoiceNo"].nunique()
total_units = filtered["Quantity"].sum()
total_countries = filtered["Country"].nunique()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"£{total_revenue:,.0f}")
c2.metric("Total Orders", f"{total_orders:,}")
c3.metric("Units Sold", f"{total_units:,}")
c4.metric("Countries", f"{total_countries:,}")

st.divider()

# Prepare chart data
filtered["Month"] = filtered["InvoiceDate"].dt.to_period("M").astype(str)
monthly = filtered.groupby("Month", as_index=False)["Revenue"].sum()

top_products = (
    filtered.groupby("Description", as_index=False)["Revenue"]
    .sum()
    .nlargest(10, "Revenue")
    .sort_values("Revenue")
)

country_sales = (
    filtered.groupby("Country", as_index=False)["Revenue"]
    .sum()
    .nlargest(10, "Revenue")
    .sort_values("Revenue")
)

left, right = st.columns(2)

with left:
    st.subheader("📈 Monthly Revenue Trend")
    fig = px.line(
        monthly,
        x="Month",
        y="Revenue",
        markers=True,
        template="plotly_white",
        title="Revenue by Month"
    )
    fig.update_layout(yaxis_title="Revenue (£)", xaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("🏆 Top 10 Products")
    fig = px.bar(
        top_products,
        x="Revenue",
        y="Description",
        orientation="h",
        template="plotly_white",
        title="Products by Revenue"
    )
    fig.update_layout(xaxis_title="Revenue (£)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("🌍 Revenue by Country")
fig = px.bar(
    country_sales,
    x="Country",
    y="Revenue",
    template="plotly_white",
    title="Top 10 Countries by Revenue"
)
st.plotly_chart(fig, use_container_width=True)

# Customer segmentation
segment_file = Path("customer_segments.csv")
if segment_file.exists():
    st.subheader("👥 Customer Segmentation (RFM)")
    segments = pd.read_csv(segment_file)

    if "Segment" in segments.columns:
        segment_counts = (
            segments["Segment"]
            .value_counts()
            .rename_axis("Segment")
            .reset_index(name="Customers")
        )
        fig = px.pie(
            segment_counts,
            names="Segment",
            values="Customers",
            hole=0.45,
            title="Customers by Segment",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Run customer_segmentation.py to add the RFM customer chart.")

# Data preview
with st.expander("🔎 Explore transaction data"):
    st.dataframe(
        filtered.sort_values("InvoiceDate", ascending=False),
        use_container_width=True
    )
    st.download_button(
        "Download filtered data as CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_retail_data.csv",
        mime="text/csv"
    )

st.caption("Data source: UCI Machine Learning Repository — Online Retail.")

st.divider()

st.header("💡 Business Insights")

best_product = filtered.groupby("Description")["Revenue"].sum().idxmax()
best_product_revenue = filtered.groupby("Description")["Revenue"].sum().max()

best_country = filtered.groupby("Country")["Revenue"].sum().idxmax()
best_country_revenue = filtered.groupby("Country")["Revenue"].sum().max()

daily_sales = filtered.groupby(
    filtered["InvoiceDate"].dt.date
)["Revenue"].sum()

best_day = daily_sales.idxmax()
best_day_revenue = daily_sales.max()

col1, col2 = st.columns(2)

with col1:
    st.success(
        f"🏆 **Top Revenue Product:** {best_product}\n\n"
        f"Revenue: £{best_product_revenue:,.2f}"
    )

    st.info(
        f"🌍 **Top Revenue Country:** {best_country}\n\n"
        f"Revenue: £{best_country_revenue:,.2f}"
    )

with col2:
    st.warning(
        f"📅 **Highest Revenue Day:** {best_day}\n\n"
        f"Revenue: £{best_day_revenue:,.2f}"
    )

    st.write(
        "### Business Recommendations"
    )
    st.write("- Monitor top-performing products and maintain stock.")
    st.write("- Study high-revenue markets to identify growth opportunities.")
    st.write("- Investigate low-performing periods and plan promotions.")
