import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
from sklearn.ensemble import RandomForestRegressor

# -----------------------------
# Load data
# -----------------------------

df = pd.read_csv("retail_features.csv")
df["sale_date"] = pd.to_datetime(df["sale_date"])

# -----------------------------
# Train model for prediction
# -----------------------------

X = df.drop(columns=["revenue", "sale_date"])
y = df["revenue"]

model = RandomForestRegressor(n_estimators=150, random_state=42)
model.fit(X, y)

# -----------------------------
# Helper: identify store type
# -----------------------------


def get_store_type(row):
    if row["store_type_Tier2"] == 1:
        return "Tier2"
    elif row["store_type_Town"] == 1:
        return "Town"
    else:
        return "Metro"


df["store_type"] = df.apply(get_store_type, axis=1)

# -----------------------------
# Dash app
# -----------------------------

app = Dash(__name__)
app.title = "Retail Sales Analytics Dashboard"

# -----------------------------
# Layout
# -----------------------------

app.layout = html.Div(
    [
        html.H1(
            "📊 Retail Sales Analytics & Forecast Dashboard",
            style={"textAlign": "center"},
        ),
        dcc.Dropdown(
            id="store_filter",
            options=[
                {"label": "Metro", "value": "Metro"},
                {"label": "Tier2", "value": "Tier2"},
                {"label": "Town", "value": "Town"},
                {"label": "All (Comparison)", "value": "All"},
            ],
            value="All",
            clearable=False,
            style={"width": "350px"},
        ),
        dcc.Graph(id="daily_trend"),
        dcc.Graph(id="monthly_seasonality"),
        dcc.Graph(id="promotion_impact"),
        html.Hr(),
        html.H3("🔮 Revenue Prediction"),
        dcc.Dropdown(
            id="pred_store",
            options=[
                {"label": "Metro", "value": "Metro"},
                {"label": "Tier2", "value": "Tier2"},
                {"label": "Town", "value": "Town"},
            ],
            value="Metro",
            style={"width": "300px"},
        ),
        dcc.Dropdown(
            id="pred_promo",
            options=[
                {"label": "Promotion", "value": 1},
                {"label": "No Promotion", "value": 0},
            ],
            value=1,
            style={"width": "300px"},
        ),
        dcc.Input(id="pred_month", type="number", placeholder="Enter Month (1-12)"),
        html.Br(),
        html.Br(),
        html.Button("Predict Revenue", id="predict_btn"),
        html.H2(id="prediction_output", style={"color": "green"}),
    ]
)

# -----------------------------
# Callbacks
# -----------------------------


@app.callback(
    Output("daily_trend", "figure"),
    Output("monthly_seasonality", "figure"),
    Output("promotion_impact", "figure"),
    Input("store_filter", "value"),
)
def update_charts(store_choice):

    if store_choice == "All":
        filtered = df
        color = "store_type"
    else:
        filtered = df[df["store_type"] == store_choice]
        color = None

    # Daily trend
    daily = filtered.groupby(["sale_date", "store_type"])["revenue"].sum().reset_index()

    fig_trend = px.line(
        daily,
        x="sale_date",
        y="revenue",
        color=color,
        title="Daily Revenue Trend Comparison",
    )

    # Monthly
    filtered["month"] = filtered["sale_date"].dt.month
    monthly = filtered.groupby(["month", "store_type"])["revenue"].sum().reset_index()

    fig_month = px.bar(
        monthly,
        x="month",
        y="revenue",
        color="store_type",
        barmode="group",
        title="Monthly Seasonality Comparison",
    )

    # Promotion
    promo = (
        filtered.groupby(["promotion", "store_type"])["revenue"].mean().reset_index()
    )

    fig_promo = px.bar(
        promo,
        x="promotion",
        y="revenue",
        color="store_type",
        barmode="group",
        title="Promotion Impact Comparison",
    )

    return fig_trend, fig_month, fig_promo


# -----------------------------
# Prediction callback
# -----------------------------


@app.callback(
    Output("prediction_output", "children"),
    Input("predict_btn", "n_clicks"),
    State("pred_store", "value"),
    State("pred_promo", "value"),
    State("pred_month", "value"),
)
def predict_revenue(n, store, promo, month):

    if not n:
        return ""

    input_data = X.iloc[0].copy()

    input_data[:] = 0
    input_data["promotion"] = promo
    input_data["month"] = month

    if store == "Tier2":
        input_data["store_type_Tier2"] = 1
    elif store == "Town":
        input_data["store_type_Town"] = 1

    prediction = model.predict([input_data.values])[0]

    return f"💰 Predicted Revenue: {round(prediction,2)}"


# -----------------------------
# Run app
# -----------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)
