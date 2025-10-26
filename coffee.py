# Business Question: Which products and times of day generate the most profit?
import pandas as pd

df = pd.read_csv('coffee.csv')
# df.info()
# df.describe()
# df.head()

df['money'] = (df['money'] * 5).round(-1)
df['Date']= pd.to_datetime(df['Date'], format ='%d/%m/%Y')
df['Day'] = df['Date'].dt.day_name()
df['Month'] = df['Date'].dt.month_name()
# Drop columns Weekday and Month_name in favour of Day and Month
# Rename columns hour_of_day
df = df.drop(['Weekday', 'Month_name'], axis=1)
df = df.rename(columns={'hour_of_day': 'hour'})
# Define custom sort order for month, day of week, and time of day
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
time_of_day_order = ['Morning', 'Afternoon', 'Night']
df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)
df['Day'] = pd.Categorical(df['Day'], categories=day_order, ordered=True)
df['Time_of_Day'] = pd.Categorical(df['Time_of_Day'], categories=time_of_day_order, ordered=True)


# Analyse key metrics (KPIs)
# Total daily revenue, average revenue per transaction, top 10 best-selling items, profitability by category, sales by hour or weekday
# df.columns
daily_sales = df.groupby('Date')['money'].sum()
monthly_sales = df.groupby('Month')['money'].sum()
hour_sales = df.groupby('hour')['money'].sum()
time_of_day_sales = df.groupby('Time_of_Day')['money'].sum()
day_of_week_sales = df.groupby('Day')['money'].sum()

top_items = df.groupby('coffee_name')['money'].sum().sort_values(ascending=False).head(10)

# daily_sales
# monthly_sales
# hour_sales
# time_of_day_sales
# day_of_week_sales
# top_items

# Build visuals
import streamlit as st
import plotly.express as px

st.title("Sample Coffee Shop Sales Dashboard")

st.info("This dashboard allows for businesses to make informed decisions based on their own data, allowing them to improve efficiency and ultimately increase profit.")

#KPI cards:total daily revenue, average sale, number of transactions
st.metric("Total Revenue", f"฿{df['money'].sum():,.0f}")
st.metric("Average Sale", f"฿{df['money'].mean():.0f}")

#Show a sample of the data
st.subheader("Data Preview")
st.dataframe(df.head(100))
st.info("This shows a sample of our data.")

#Bar Chart: revenue by product (coffee_name)
st.subheader("Total Revenue by Coffee Type")
fig = px.bar(
    df.groupby('coffee_name')['money'].sum().reset_index().sort_values('money', ascending=False), x='coffee_name',
    y='money',
    #title='Total Revenue by Coffee Type',
    labels={'money':'Total Revenue', 'coffee_name':'Coffee Type'}
)
st.plotly_chart(fig)
st.info("Latte is the biggest seller, followed by Americano with milk.")

#Donut chart: sales by cash_type (payment method)
sales_by_cash_type = df.groupby("cash_type")["money"].sum().reset_index()

fig = px.pie(
    sales_by_cash_type,
    names="cash_type",
    values="money",
    #title="Sales by Payment Type",
    hole=0.5,
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig.update_traces(textinfo="percent+label")

st.subheader("Sales Breakdown by Payment Type")
st.plotly_chart(fig)

st.info("All sales are made via card, suggesting customers prefer cashless payment methods.")

#Line chart: total revenue by Hour
st.subheader("Average Revenue by Hour")
daily_sales = df.groupby('hour')['money'].mean().reset_index().sort_values('hour')


fig_date = px.line(
    daily_sales,
    x='hour',
    y='money',
    # title='Revenue by Hour',
    labels={'hour':'Hour of the Day', 'money':'Average Revenue'})

st.plotly_chart(fig_date)
st.success("On average, more money is spent in from 4pm onwards.")
st.warning("Sales are lower in the morning; consider promotions.")

#Line chart: total revenue by Day
st.subheader("Average Revenue by Day")
daily_sales = df.groupby('Day')['money'].sum().reset_index().sort_values('Day')
date_sales = df.groupby('Date')['money'].sum().reset_index()
date_sales['Day'] = date_sales['Date'].dt.day_name()
avg_sales_by_day = date_sales.groupby('Day')['money'].mean().reset_index()
avg_sales_by_day['Day'] = pd.Categorical(avg_sales_by_day['Day'], categories=day_order, ordered=True)
avg_sales_by_day = avg_sales_by_day.sort_values('Day')


fig_date = px.line(
    avg_sales_by_day,
    x='Day',
    y='money',
    #title='Revenue by Day',
    labels={"money":"Average Revenue"})
st.plotly_chart(fig_date)
st.success("Peak sales occur on Monday and Tuesday - ideal for promoting combo deals.")
st.warning("Sales are lower on weekends; consider promotions.")

#Line chart: Sales by Month
st.subheader("Monthly Sales")
monthly_sales = df.groupby('Month')['money'].sum().reset_index().sort_values('Month')
fig_month = px.line(
    monthly_sales,
    x='Month',
    y='money',
    #title='Revenue by Month',
    labels={'money':'Money'})
st.plotly_chart(fig_month)

st.success("Peak sales occur in March and October.")
st.warning("Sales are lower in January and April; consider promotions.")

#Insights text box
st.subheader("Key Insights")
st.success("Peak sales occur in the evenings, on Mondays and Tuesdays, and in March and October. These are the best times to consider upselling and/or cross-selling e.g. premium versions or combo versions.")
st.warning("Sales are lower in the morning, on weekends, and January and April. Consider running promotions e.g. \"student\" days with small discounts, launch seasonal menu items, or early-bird/night-owl offers.")

st.markdown(
    """
    <hr style="margin-top: 40px; border-color: #333;">
    <div style="text-align: right; color: #ccc; font-size:0.8em;">
        Dashboard designed by <a href="https://www.linkedin.com/in/cillian-d-030860101" target="_blank" style="color: #ccc; text-decoration: none;"><b>Cillian</></a>
    </div>
    """,
    unsafe_allow_html=True
)