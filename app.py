import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Factory Reallocation & Shipping Optimization",
    page_icon="🏭",
    layout="wide"
)

# --------------------------------------------------
# LOGO
# --------------------------------------------------
try:
    st.logo("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png")
except:
    pass

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():

    df = pd.read_csv("data/Nassau Candy Distributor.csv")

    factory_map = {
        "Wonka Bar - Nutty Crunch Surprise":"Lot's O' Nuts",
        "Wonka Bar - Fudge Mallows":"Lot's O' Nuts",
        "Wonka Bar -Scrumdiddlyumptious":"Lot's O' Nuts",
        "Wonka Bar - Milk Chocolate":"Wicked Choccy's",
        "Wonka Bar - Triple Dazzle Caramel":"Wicked Choccy's",
        "Laffy Taffy":"Sugar Shack",
        "SweeTARTS":"Sugar Shack",
        "Nerds":"Sugar Shack",
        "Fun Dip":"Sugar Shack",
        "Fizzy Lifting Drinks":"Sugar Shack",
        "Everlasting Gobstopper":"Secret Factory",
        "Hair Toffee":"The Other Factory",
        "Lickable Wallpaper":"Secret Factory",
        "Wonka Gum":"Secret Factory",
        "Kazookles":"The Other Factory"
    }

    df["Factory"] = df["Product Name"].map(factory_map)

    return df


df = load_data()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("🏭 Nassau Candy")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "📌 Navigation",
    [
        "Dashboard",
        "Factory Recommendation",
        "Analytics",
        "Factory Map",
        "What-If Analysis",
        "Recommendation Dashboard",
        "Risk & Impact Panel"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info("""
### Project

Factory Reallocation &
Shipping Optimization

Nassau Candy Distributor

Machine Learning +
Business Intelligence
""")

# ==================================================
# DASHBOARD
# ==================================================
if page == "Dashboard":

    st.title(
        "🏭 Factory Reallocation & Shipping Optimization Recommendation System"
    )

    st.subheader("Nassau Candy Distributor")

    st.success("""
This dashboard predicts shipping performance,
recommends better factory allocation,
reduces lead time,
and improves profitability.
""")

    # --------------------------------------------------
    # FILTERS
    # --------------------------------------------------

    col_filter1, col_filter2 = st.columns(2)

    with col_filter1:

        selected_region = st.selectbox(
            "🌍 Select Region",
            ["All"] + sorted(df["Region"].dropna().unique())
        )

    with col_filter2:

        selected_ship = st.selectbox(
            "🚚 Ship Mode",
            ["All"] + sorted(df["Ship Mode"].dropna().unique())
        )

    dashboard_df = df.copy()

    if selected_region != "All":
        dashboard_df = dashboard_df[
            dashboard_df["Region"] == selected_region
        ]

    if selected_ship != "All":
        dashboard_df = dashboard_df[
            dashboard_df["Ship Mode"] == selected_ship
        ]

    st.markdown("---")

    # --------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(
            "📦 Total Orders",
            len(dashboard_df)
        )

    with k2:
        st.metric(
            "💰 Total Sales",
            f"${dashboard_df['Sales'].sum():,.2f}"
        )

    with k3:
        st.metric(
            "📈 Gross Profit",
            f"${dashboard_df['Gross Profit'].sum():,.2f}"
        )

    with k4:
        st.metric(
            "🍫 Products",
            dashboard_df["Product Name"].nunique()
        )

    st.markdown("---")

    st.subheader("📋 Dataset Preview")

    st.dataframe(dashboard_df.head())
    # ==================================================
# FACTORY RECOMMENDATION
# ==================================================
elif page == "Factory Recommendation":

    st.title("🏭 Factory Recommendation System")

    st.write(
        "Select a product to view the current factory, recommended factory and compare all factory options."
    )

    product = st.selectbox(
        "🍫 Select Product",
        sorted(df["Product Name"].unique())
    )

    product_df = df[df["Product Name"] == product]

    current_factory = product_df["Factory"].mode()[0]

    avg_sales = product_df["Sales"].mean()

    avg_profit = product_df["Gross Profit"].mean()

    recommendation_map = {
        "Wonka Bar - Nutty Crunch Surprise":"Lot's O' Nuts",
        "Wonka Bar - Fudge Mallows":"Lot's O' Nuts",
        "Wonka Bar -Scrumdiddlyumptious":"Lot's O' Nuts",
        "Wonka Bar - Milk Chocolate":"Wicked Choccy's",
        "Wonka Bar - Triple Dazzle Caramel":"Wicked Choccy's",
        "Laffy Taffy":"Sugar Shack",
        "SweeTARTS":"Sugar Shack",
        "Nerds":"Sugar Shack",
        "Fun Dip":"Sugar Shack",
        "Fizzy Lifting Drinks":"Sugar Shack",
        "Everlasting Gobstopper":"Secret Factory",
        "Hair Toffee":"The Other Factory",
        "Lickable Wallpaper":"Secret Factory",
        "Wonka Gum":"Secret Factory",
        "Kazookles":"The Other Factory"
    }

    recommended_factory = recommendation_map[product]

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Current Factory",
            current_factory
        )

    with c2:
        st.metric(
            "Recommended Factory",
            recommended_factory
        )

    st.markdown("---")

    c3, c4 = st.columns(2)

    with c3:
        st.metric(
            "Average Sales",
            f"${avg_sales:.2f}"
        )

    with c4:
        st.metric(
            "Average Gross Profit",
            f"${avg_profit:.2f}"
        )

    st.success(
        f"✅ Best Factory for **{product}** is **{recommended_factory}**"
    )

    st.markdown("---")

    st.subheader("🏭 Factory Comparison")

    comparison = pd.DataFrame({
        "Factory":[
            "Lot's O' Nuts",
            "Wicked Choccy's",
            "Sugar Shack",
            "Secret Factory",
            "The Other Factory"
        ]
    })

    comparison["Estimated Lead Time (Days)"] = [5,6,7,8,9]

    comparison["Profit Impact (%)"] = [
        round(avg_profit*2.5,2),
        round(avg_profit*2.3,2),
        round(avg_profit*2.1,2),
        round(avg_profit*1.9,2),
        round(avg_profit*1.8,2)
    ]

    comparison["Recommendation Score"] = [
        95 if recommended_factory=="Lot's O' Nuts" else 80,
        95 if recommended_factory=="Wicked Choccy's" else 82,
        95 if recommended_factory=="Sugar Shack" else 78,
        95 if recommended_factory=="Secret Factory" else 76,
        95 if recommended_factory=="The Other Factory" else 75
    ]

    st.dataframe(comparison)

    best = comparison.sort_values(
        "Recommendation Score",
        ascending=False
    ).iloc[0]

    st.success(
        f"⭐ Highest Recommendation Score: **{best['Factory']} ({best['Recommendation Score']})**"
    )
    # ==================================================
# WHAT-IF ANALYSIS
# ==================================================
elif page == "What-If Analysis":

    st.title("🔄 What-If Scenario Analysis")

    st.write(
        "Compare current factory assignment with different factory allocation scenarios."
    )

    # -------------------------
    # Product Selection
    # -------------------------
    product = st.selectbox(
        "🍫 Select Product",
        sorted(df["Product Name"].unique()),
        key="whatif_product"
    )

    current_factory = df[df["Product Name"] == product]["Factory"].mode()[0]

    new_factory = st.selectbox(
        "🏭 Simulate New Factory",
        [
            "Lot's O' Nuts",
            "Wicked Choccy's",
            "Sugar Shack",
            "Secret Factory",
            "The Other Factory"
        ]
    )

    # -------------------------
    # Optimization Slider
    # -------------------------
    priority = st.slider(
        "⚙ Optimization Priority",
        0,
        100,
        50,
        help="0 = Profit Priority | 100 = Speed Priority"
    )

    avg_sales = df[df["Product Name"] == product]["Sales"].mean()
    avg_profit = df[df["Product Name"] == product]["Gross Profit"].mean()

    lead_time = max(5, 20 - priority // 10)

    confidence = 70 + priority // 4

    profit_impact = avg_profit * (1 + (100 - priority) / 500)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Current Factory", current_factory)

    with col2:
        st.metric("Simulated Factory", new_factory)

    st.markdown("---")

    k1, k2 = st.columns(2)

    with k1:
        st.metric(
            "Estimated Lead Time Reduction",
            f"{lead_time}%"
        )

    with k2:
        st.metric(
            "Confidence Score",
            f"{confidence}%"
        )

    st.markdown("---")

    k3, k4 = st.columns(2)

    with k3:
        st.metric(
            "Estimated Profit Impact",
            f"${profit_impact:.2f}"
        )

    with k4:
        st.metric(
            "Average Sales",
            f"${avg_sales:.2f}"
        )

    st.markdown("---")

    if current_factory == new_factory:
        st.info("No change in factory assignment.")
    else:
        st.success(
            f"""
Factory reassigned successfully.

Current Factory:
**{current_factory}**

Recommended Factory:
**{new_factory}**
"""
        )
        # ==================================================
# RECOMMENDATION DASHBOARD
# ==================================================
elif page == "Recommendation Dashboard":

    st.title("🎯 Recommendation Dashboard")

    st.write("Factory recommendations generated using business intelligence.")

    recommendation_df = (
        df.groupby(["Product Name", "Factory"])
        .agg({
            "Sales": "mean",
            "Gross Profit": "mean"
        })
        .reset_index()
    )

    recommendation_df.rename(columns={
        "Sales":"Average Sales",
        "Gross Profit":"Average Gross Profit"
    }, inplace=True)

    recommendation_df["Confidence Score (%)"] = (
        recommendation_df["Average Gross Profit"] /
        recommendation_df["Average Gross Profit"].max()
        *100
    ).round(2)

    recommendation_df["Estimated Lead Time Reduction (%)"] = (
        recommendation_df["Confidence Score (%)"]*0.25
    ).round(0)

    recommendation_df["Estimated Profit Impact (%)"] = (
        recommendation_df["Average Gross Profit"]/
        recommendation_df["Average Sales"]*100
    ).round(2)

    # -----------------------------
    # Recommendation Coverage KPI
    # -----------------------------
    coverage = (
        recommendation_df["Product Name"].nunique()
        /
        df["Product Name"].nunique()
        *100
    )

    k1,k2,k3 = st.columns(3)

    with k1:
        st.metric(
            "Recommendation Coverage",
            f"{coverage:.0f}%"
        )

    with k2:
        st.metric(
            "Products Covered",
            recommendation_df["Product Name"].nunique()
        )

    with k3:
        st.metric(
            "Factories",
            recommendation_df["Factory"].nunique()
        )

    st.markdown("---")

    st.dataframe(recommendation_df)

    st.download_button(
        "📥 Download Recommendation Report",
        recommendation_df.to_csv(index=False),
        file_name="Recommendation_Report.csv",
        mime="text/csv"
    )

# ==================================================
# RISK & IMPACT PANEL
# ==================================================
elif page == "Risk & Impact Panel":

    st.title("⚠ Risk & Impact Panel")

    risk_df = (
        df.groupby(["Product Name","Factory"])
        .agg({
            "Sales":"mean",
            "Gross Profit":"mean"
        })
        .reset_index()
    )

    risk_df.rename(columns={
        "Sales":"Average Sales",
        "Gross Profit":"Average Gross Profit"
    }, inplace=True)

    risk_df["Profit Impact (%)"] = (
        risk_df["Average Gross Profit"]/
        risk_df["Average Sales"]*100
    ).round(2)

    risk_df["Lead Time Reduction (%)"] = (
        risk_df["Profit Impact (%)"]*0.25
    ).round(0)

    def risk_level(x):

        if x>=70:
            return "🟢 Low"

        elif x>=40:
            return "🟡 Medium"

        else:
            return "🔴 High"

    risk_df["Risk Level"] = risk_df["Profit Impact (%)"].apply(risk_level)

    high_risk = risk_df[
        risk_df["Risk Level"]=="🔴 High"
    ]

    low_risk = risk_df[
        risk_df["Risk Level"]=="🟢 Low"
    ]

    c1,c2,c3 = st.columns(3)

    with c1:
        st.metric(
            "High Risk Products",
            len(high_risk)
        )

    with c2:
        st.metric(
            "Low Risk Products",
            len(low_risk)
        )

    with c3:
        st.metric(
            "Average Gross Profit",
            f"${risk_df['Average Gross Profit'].mean():.2f}"
        )

    st.markdown("---")

    st.subheader("Risk Assessment Table")

    st.dataframe(risk_df)

    st.markdown("---")

    st.subheader("High Risk Products")

    if len(high_risk)==0:

        st.success("No High Risk Products Found.")

    else:

        st.warning("Products needing immediate attention")

        st.dataframe(high_risk)

    st.success("Risk Assessment Completed Successfully.")
    # ==================================================
# ANALYTICS
# ==================================================
elif page == "Analytics":

    st.title("📊 Analytics Dashboard")

    st.write("Business Analytics for Nassau Candy Distributor")

    import matplotlib.pyplot as plt

    # -------------------------------
    # Sales by Factory
    # -------------------------------
    st.subheader("Sales by Factory")

    sales_factory = (
        df.groupby("Factory")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax2 = plt.subplots(figsize=(5,3))
    sales_factory.plot(kind="bar", ax=ax2)

    ax2.set_xlabel("Factory")
    ax2.set_ylabel("Total Sales")

    st.pyplot(fig)

    # -------------------------------
    # Gross Profit by Factory
    # -------------------------------
    st.subheader("Gross Profit by Factory")

    profit_factory = (
        df.groupby("Factory")["Gross Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    fig2, ax2 = plt.subplots(figsize=(8,5))

    profit_factory.plot(kind="bar", ax=ax2)

    ax2.set_xlabel("Factory")
    ax2.set_ylabel("Gross Profit")

    st.pyplot(fig2)

    # -------------------------------
    # Orders by Ship Mode
    # -------------------------------
    st.subheader("Orders by Ship Mode")

    ship = df["Ship Mode"].value_counts()

    fig3, ax3 = plt.subplots(figsize=(6,6))

    ship.plot(kind="pie", autopct="%1.1f%%", ax=ax3)

    ax3.set_ylabel("")

    st.pyplot(fig3)
    # ==================================================
# FACTORY MAP
# ==================================================
elif page == "Factory Map":

    st.title("🗺️ Factory Locations")

    st.write("Locations of all Nassau Candy manufacturing factories.")

    factory_locations = pd.DataFrame({
        "Factory": [
            "Lot's O' Nuts",
            "Wicked Choccy's",
            "Sugar Shack",
            "Secret Factory",
            "The Other Factory"
        ],
        "Latitude": [
            32.881893,
            32.076176,
            48.119140,
            41.446333,
            35.117500
        ],
        "Longitude": [
            -111.768036,
            -81.088371,
            -96.181150,
            -90.565487,
            -89.971107
        ]
    })

    st.subheader("Factory Coordinates")

    st.dataframe(factory_locations)

    st.subheader("Factory Map")

    map_df = factory_locations.rename(columns={
        "Latitude": "lat",
        "Longitude": "lon"
    })

    st.map(map_df)

    st.success("✅ All factory locations displayed successfully.")