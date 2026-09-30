import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Veda Technology Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f7f8fa;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.metric-card {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e6e6e6;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.dashboard-title {
    font-size: 32px;
    font-weight: 700;
}

.dashboard-subtitle {
    color: #666666;
    font-size: 16px;
}

.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    path = "data/processed/veda_technology_business_clean.csv"

    data = pd.read_csv(path)

    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(
            data["Date"],
            errors="coerce"
        )

    return data


try:

    df = load_data()

except Exception as e:

    st.error(
        "Unable to load the cleaned dataset. "
        "Please check that the CSV exists at "
        "`data/processed/veda_technology_business_clean.csv`."
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">'
    'Veda Technology Business & Service Analytics'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Executive Business Intelligence Dashboard '
    'based on simulated business data'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("Dashboard Filters")

filtered_df = df.copy()


# City
if "City" in df.columns:

    cities = sorted(
        df["City"].dropna().unique()
    )

    selected_cities = st.sidebar.multiselect(
        "City",
        cities,
        default=cities
    )

    filtered_df = filtered_df[
        filtered_df["City"].isin(selected_cities)
    ]


# Marketing Channel
if "Marketing_Channel" in df.columns:

    channels = sorted(
        df["Marketing_Channel"].dropna().unique()
    )

    selected_channels = st.sidebar.multiselect(
        "Marketing Channel",
        channels,
        default=channels
    )

    filtered_df = filtered_df[
        filtered_df["Marketing_Channel"].isin(
            selected_channels
        )
    ]


# Customer Type
if "Customer_Type" in df.columns:

    customer_types = sorted(
        df["Customer_Type"].dropna().unique()
    )

    selected_customer_types = st.sidebar.multiselect(
        "Customer Type",
        customer_types,
        default=customer_types
    )

    filtered_df = filtered_df[
        filtered_df["Customer_Type"].isin(
            selected_customer_types
        )
    ]


# Inquiry Type
if "Inquiry_Type" in df.columns:

    inquiry_types = sorted(
        df["Inquiry_Type"].dropna().unique()
    )

    selected_inquiries = st.sidebar.multiselect(
        "Inquiry Type",
        inquiry_types,
        default=inquiry_types
    )

    filtered_df = filtered_df[
        filtered_df["Inquiry_Type"].isin(
            selected_inquiries
        )
    ]


# Service Category
if "Service_Category" in df.columns:

    categories = sorted(
        df["Service_Category"].dropna().unique()
    )

    selected_categories = st.sidebar.multiselect(
        "Service Category",
        categories,
        default=categories
    )

    filtered_df = filtered_df[
        filtered_df["Service_Category"].isin(
            selected_categories
        )
    ]


st.sidebar.divider()

st.sidebar.write(
    f"**Records displayed:** {len(filtered_df):,}"
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_visitors = int(
    filtered_df["Website_Visit"].sum()
)

total_inquiries = len(filtered_df)

total_service_requests = int(
    filtered_df["Service_Request"].sum()
)

total_revenue = float(
    filtered_df["Revenue"].sum()
)

total_conversions = int(
    filtered_df["Conversion"].sum()
)

conversion_rate = (
    total_conversions / total_visitors * 100
    if total_visitors > 0
    else 0
)

avg_satisfaction = float(
    filtered_df["Satisfaction_Score"].mean()
)

avg_response_time = float(
    filtered_df["Response_Time_Hours"].mean()
)


# ============================================================
# KPI CARDS
# ============================================================

st.markdown(
    '<div class="section-title">Executive KPIs</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Website Visitors",
        f"{total_visitors:,}"
    )


with col2:

    st.metric(
        "Total Inquiries",
        f"{total_inquiries:,}"
    )


with col3:

    st.metric(
        "Service Requests",
        f"{total_service_requests:,}"
    )


with col4:

    st.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}"
    )


with col5:

    st.metric(
        "Conversion Rate",
        f"{conversion_rate:.2f}%"
    )


# ============================================================
# SECONDARY KPIs
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Conversions",
        f"{total_conversions:,}"
    )

with col2:

    st.metric(
        "Avg. Satisfaction",
        f"{avg_satisfaction:.2f}/5"
    )

with col3:

    st.metric(
        "Avg. Response Time",
        f"{avg_response_time:.2f} hrs"
    )


st.divider()


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Business Overview",
        "👥 Customer Analytics",
        "🛠️ Service Analytics",
        "🎓 Marketing & Training"
    ]
)


# ============================================================
# TAB 1 — BUSINESS OVERVIEW
# ============================================================

with tab1:

    st.subheader("Business Performance Overview")

    col1, col2 = st.columns(2)

    # Marketing
    with col1:

        marketing = (
            filtered_df
            .groupby("Marketing_Channel")
            .agg(
                Visitors=("Website_Visit", "sum"),
                Conversions=("Conversion", "sum"),
                Revenue=("Revenue", "sum")
            )
            .reset_index()
        )

        fig = px.bar(
            marketing,
            x="Marketing_Channel",
            y="Visitors",
            title="Website Visitors by Marketing Channel",
            text_auto=True
        )

        fig.update_layout(
            xaxis_title="Marketing Channel",
            yaxis_title="Visitors",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Revenue
    with col2:

        marketing_revenue = (
            filtered_df
            .groupby("Marketing_Channel")["Revenue"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            marketing_revenue,
            x="Marketing_Channel",
            y="Revenue",
            title="Revenue by Marketing Channel",
            text_auto=".2s"
        )

        fig.update_layout(
            xaxis_title="Marketing Channel",
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Monthly trend
    if "Date" in filtered_df.columns:

        monthly = (
            filtered_df
            .dropna(subset=["Date"])
            .assign(
                Month=lambda x:
                x["Date"].dt.to_period("M").astype(str)
            )
            .groupby("Month")
            .agg(
                Revenue=("Revenue", "sum"),
                Requests=("Service_Request", "sum")
            )
            .reset_index()
        )

        fig = px.line(
            monthly,
            x="Month",
            y="Revenue",
            markers=True,
            title="Monthly Revenue Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# TAB 2 — CUSTOMER ANALYTICS
# ============================================================

with tab2:

    st.subheader("Customer Analytics")

    col1, col2 = st.columns(2)


    # Customer type
    with col1:

        customer_analysis = (
            filtered_df
            .groupby("Customer_Type")
            .agg(
                Customers=("Customer_ID", "count"),
                Revenue=("Revenue", "sum"),
                Satisfaction=("Satisfaction_Score", "mean")
            )
            .reset_index()
        )

        fig = px.bar(
            customer_analysis,
            x="Customer_Type",
            y="Customers",
            title="Customers by Customer Type",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Satisfaction
    with col2:

        satisfaction = (
            filtered_df
            .groupby("Customer_Type")
            ["Satisfaction_Score"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            satisfaction,
            x="Customer_Type",
            y="Satisfaction_Score",
            title="Average Satisfaction by Customer Type",
            text_auto=".2f"
        )

        fig.update_layout(
            yaxis_title="Average Satisfaction"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# TAB 3 — SERVICE ANALYTICS
# ============================================================

with tab3:

    st.subheader("Service Demand & Performance")

    service_analysis = (
        filtered_df
        .groupby("Service")
        .agg(
            Requests=("Service_Request", "sum"),
            Revenue=("Revenue", "sum"),
            Satisfaction=("Satisfaction_Score", "mean"),
            Response_Time=("Response_Time_Hours", "mean")
        )
        .reset_index()
        .sort_values(
            "Requests",
            ascending=False
        )
    )

    col1, col2 = st.columns(2)


    with col1:

        fig = px.bar(
            service_analysis,
            x="Requests",
            y="Service",
            orientation="h",
            title="Service Demand",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        fig = px.bar(
            service_analysis,
            x="Service",
            y="Satisfaction",
            title="Service Satisfaction",
            text_auto=".2f"
        )

        fig.update_layout(
            xaxis_tickangle=-45
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.subheader("Service Performance Table")

    display_table = service_analysis.copy()

    display_table["Revenue"] = (
        display_table["Revenue"]
        .round(2)
    )

    display_table["Satisfaction"] = (
        display_table["Satisfaction"]
        .round(2)
    )

    display_table["Response_Time"] = (
        display_table["Response_Time"]
        .round(2)
    )

    st.dataframe(
        display_table,
        use_container_width=True
    )


# ============================================================
# TAB 4 — MARKETING & TRAINING
# ============================================================

with tab4:

    st.subheader(
        "Marketing, Internship & Training Analytics"
    )

    col1, col2 = st.columns(2)


    # Internship
    with col1:

        internship = filtered_df[
            filtered_df["Inquiry_Type"]
            == "Internship"
        ]

        if len(internship) > 0:

            application_status = (
                internship
                ["Application_Status"]
                .value_counts()
                .reset_index()
            )

            application_status.columns = [
                "Application_Status",
                "Count"
            ]

            fig = px.pie(
                application_status,
                names="Application_Status",
                values="Count",
                title="Internship Application Status"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No internship records match "
                "the current filters."
            )


    # Training
    with col2:

        training = (
            filtered_df
            .groupby("Training_Program")
            .agg(
                Enrollments=("Training_Enrollment", "sum"),
                Completions=("Training_Completion", "sum"),
                Avg_Score=("Training_Score", "mean")
            )
            .reset_index()
        )

        fig = px.bar(
            training,
            x="Training_Program",
            y="Avg_Score",
            title="Training Program Performance",
            text_auto=".1f"
        )

        fig.update_layout(
            xaxis_tickangle=-45
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.subheader("Training Performance Table")

    st.dataframe(
        training,
        use_container_width=True
    )


# ============================================================
# DATA PREVIEW
# ============================================================

st.divider()

with st.expander("View Dataset"):

    st.dataframe(
        filtered_df.head(100),
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Veda Technology Business & Service Analytics | "
    "Synthetic dataset | Data Science Internship Project"
)