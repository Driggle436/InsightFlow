import streamlit as st


def render_sidebar_filters(sales):
  st.sidebar.markdown("### InsightFlow")
  st.sidebar.caption("Business intelligence")

  persona = st.sidebar.selectbox(
    "View as",
    ["CEO", "Sales Manager", "Analyst"],
  )

  st.sidebar.divider()
  st.sidebar.markdown("**Filters**")

  min_date = sales["date"].min()
  max_date = sales["date"].max()

  date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
  )

  regions = ["All"] + sorted(sales["region"].unique().tolist())
  selected_region = st.sidebar.selectbox("Region", regions)

  products = ["All"] + sorted(sales["product"].unique().tolist())
  selected_product = st.sidebar.selectbox("Product", products)

  st.sidebar.divider()
  st.sidebar.markdown("**Pages**")
  st.sidebar.page_link("app.py", label="Overview", icon="🏠")
  st.sidebar.page_link("pages/1_Insights.py", label="Insights", icon="💡")
  st.sidebar.page_link("pages/2_Actions.py", label="Actions", icon="🚀")
  st.sidebar.page_link("pages/3_Feedback.py", label="Feedback", icon="📝")
  st.sidebar.page_link("pages/9_Engine_Room.py", label="Engine Room", icon="⚙️")

  return persona, date_range, selected_region, selected_product
