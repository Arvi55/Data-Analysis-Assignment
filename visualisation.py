import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.io as pio

pio.templates.default = "plotly_white"

hourly_data = pd.read_csv(r"C:\Users\avina\OneDrive\Desktop\code program\hourly.csv")
daily_data = pd.read_csv(r"C:\Users\avina\OneDrive\Desktop\code program\daily.csv")
total_data = pd.read_csv(r"C:\Users\avina\OneDrive\Desktop\code program\total.csv")

print(hourly_data.head())
print(daily_data.head())
print(total_data.head())

for df in [hourly_data, daily_data, total_data]:
    for col in df.columns:
        if df[col].dtype != 'object':  # only numeric columns
            df[col].fillna(df[col].mean(), inplace=True)

ivt_data = hourly_data.merge(daily_data, how='outer').merge(total_data, how='outer')
ivt_data = ivt_data.reset_index(drop=True)
print(ivt_data.head())



# 1️⃣ Scatter: Requests vs Impressions colored by IVT
figure = px.scatter(
    data_frame=ivt_data,
    x="total_requests",
    y="impressions",
    size="total_requests",
    color="ivt",
    title="Total Requests vs Impressions (Colored by IVT)"
)
figure.show()

# 2️⃣ Pie: IVT contribution
labels = ["Total IVT from Hourly", "Total IVT from Daily", "Total IVT from Total"]
counts = [
    hourly_data["ivt"].sum() if "ivt" in hourly_data.columns else 0,
    daily_data["ivt"].sum() if "ivt" in daily_data.columns else 0,
    total_data["ivt"].sum() if "ivt" in total_data.columns else 0
]
colors = ['gold','lightgreen','lightblue']
fig = go.Figure(data=[go.Pie(labels=labels, values=counts)])
fig.update_layout(title_text='IVT Contribution')
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='black', width=2)))
fig.show()

# 3️⃣ Trendline: Requests vs IVT
sns.lmplot(
    data=ivt_data,
    x="total_requests",
    y="ivt",
    aspect=1.5
)
plt.title("Trendline: Total Requests vs IVT")
plt.tight_layout()
plt.show()

# 4️⃣ Trendline: Impressions vs IVT
sns.lmplot(
    data=ivt_data,
    x="impressions",
    y="ivt",
    aspect=1.5
)
plt.title("Trendline: Impressions vs IVT")
plt.tight_layout()
plt.show()

print("\n✅ Simple IVT Analysis Completed!")
