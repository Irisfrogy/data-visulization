import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# ===========================
# Data and configuration
# ===========================
DATA_PATH = "airbnb_cleaned.csv"
PRICE_AXIS_MAX = 600  # y-axis max for price charts

df = pd.read_csv(DATA_PATH)
df = df[df["price"] > 0].copy()

# Airbnb-like colors
AIRBNB_CORAL = "#FF5A5F"
AIRBNB_CORAL_DARK = "#ff9286"
AIRBNB_LIGHT_GREY = "#a3cef1"
AIRBNB_MED_GREY = "#767676"
AIRBNB_DARK = "#111111"

# Consistent borough color mapping
borough_colors = {
    "Manhattan":     AIRBNB_CORAL,
    "Brooklyn":      AIRBNB_CORAL_DARK,
    "Queens":        AIRBNB_LIGHT_GREY,
    "Bronx":         AIRBNB_MED_GREY,
    "Staten Island": AIRBNB_DARK,
}

neigh_groups = sorted(df["neighbourhood_group"].dropna().unique().tolist())
room_types = sorted(df["room_type"].dropna().unique().tolist())

neigh_options = [{"label": "All", "value": "All"}] + [
    {"label": g, "value": g} for g in neigh_groups
]

room_type_options = [{"label": "All", "value": "All"}] + [
    {"label": rt, "value": rt} for rt in room_types
]

price_ceiling_options = [
    {"label": "No limit", "value": "none"},
    {"label": "$200", "value": 200},
    {"label": "$400", "value": 400},
    {"label": "$600", "value": 600},
    {"label": "$800", "value": 800},
    {"label": "$1000", "value": 1000},
]

# New, bigger hero image
AIRBNB_LOGO_URL = (
    "https://popsop.com/wp-content/uploads/airbnb_new-logo-2014.png"
)

# ===========================
# App and layout
# ===========================
app = Dash(__name__)

server = app.server

app.layout = html.Div(
    style={
        "fontFamily": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "margin": "0 auto",
        "maxWidth": "1100px",
        "padding": "10px",
        "backgroundColor": "#F5F5F7",
    },
    children=[
        # Header with big hero image on top-right
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "backgroundColor": AIRBNB_CORAL,
                "color": "white",
                # "borderRadius": "10px",
                "padding": "14px 18px",
                "marginBottom": "10px",
                # "boxShadow": "0 2px 6px rgba(0,0,0,0.12)",
            },
            children=[
                html.Div(
                    children=[
                        html.H1(
                            "NYC Airbnb Tourist Dashboard",
                            style={
                                "margin": "0 0 6px 0",
                                "fontSize": "26px",
                                "fontWeight": "700",
                            },
                        ),
                        html.P(
                            "Compare prices, budget options, and neighbourhoods when choosing an Airbnb in New York City.",
                            style={"margin": "0", "fontSize": "13px", "opacity": 0.92},
                        ),
                    ]
                ),
                html.Img(
                    src=AIRBNB_LOGO_URL,
                    style={
                        "height": "100px",          # bigger hero image
                        "maxWidth": "300px",
                        "objectFit": "fit",
                        "marginLeft": "18px",
                        "borderRadius": "10px",
                        "boxShadow": "0 2px 6px rgba(0,0,0,0.35)",
                        "backgroundColor": "white",
                    },
                ),
            ],
        ),

        # Global filters
        html.Div(
            style={
                "display": "flex",
                "gap": "10px",
                "flexWrap": "wrap",
                "marginBottom": "8px",
            },
            children=[
                html.Div(
                    style={"flex": "1", "minWidth": "200px"},
                    children=[
                        html.Label(
                            "Neighbourhood Group",
                            style={"fontSize": "12px", "color": "#333", "fontWeight": "600"},
                        ),
                        dcc.Dropdown(
                            id="global_neigh_group",
                            options=neigh_options,
                            value="All",
                            clearable=False,
                        ),
                    ],
                ),
                html.Div(
                    style={"flex": "1", "minWidth": "200px"},
                    children=[
                        html.Label(
                            "Room Type",
                            style={"fontSize": "12px", "color": "#333", "fontWeight": "600"},
                        ),
                        dcc.Dropdown(
                            id="global_room_type",
                            options=room_type_options,
                            value="All",
                            clearable=False,
                        ),
                    ],
                ),
                html.Div(
                    style={"flex": "1", "minWidth": "200px"},
                    children=[
                        html.Label(
                            "Price Ceiling",
                            style={"fontSize": "12px", "color": "#333", "fontWeight": "600"},
                        ),
                        dcc.Dropdown(
                            id="global_price_ceiling",
                            options=price_ceiling_options,
                            value=800,
                            clearable=False,
                        ),
                    ],
                ),
            ],
        ),

        # KPI row
        html.Div(
            style={
                "display": "flex",
                "gap": "10px",
                "flexWrap": "wrap",
                "marginBottom": "8px",
            },
            children=[
                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "200px",
                        "backgroundColor": "white",
                        "borderRadius": "8px",
                        "padding": "6px 10px",
                        "boxShadow": "0 1px 3px rgba(0,0,0,0.06)",
                        "borderTop": f"3px solid {AIRBNB_CORAL}",
                    },
                    children=[
                        html.Div("Average Price", style={"fontSize": "11px", "color": "#777"}),
                        html.H2(
                            id="kpi_avg_price",
                            style={"margin": "2px 0 0 0", "fontSize": "20px"},
                        ),
                    ],
                ),
                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "200px",
                        "backgroundColor": "white",
                        "borderRadius": "8px",
                        "padding": "6px 10px",
                        "boxShadow": "0 1px 3px rgba(0,0,0,0.06)",
                        "borderTop": f"3px solid {AIRBNB_CORAL_DARK}",
                    },
                    children=[
                        html.Div("Number of Listings", style={"fontSize": "11px", "color": "#777"}),
                        html.H2(
                            id="kpi_num_listings",
                            style={"margin": "2px 0 0 0", "fontSize": "20px"},
                        ),
                    ],
                ),
                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "200px",
                        "backgroundColor": "white",
                        "borderRadius": "8px",
                        "padding": "6px 10px",
                        "boxShadow": "0 1px 3px rgba(0,0,0,0.06)",
                        "borderTop": f"3px solid {AIRBNB_MED_GREY}",
                    },
                    children=[
                        html.Div(
                            "Average Minimum Nights",
                            style={"fontSize": "11px", "color": "#777"},
                        ),
                        html.H2(
                            id="kpi_avg_min_nights",
                            style={"margin": "2px 0 0 0", "fontSize": "20px"},
                        ),
                    ],
                ),
            ],
        ),

        # TOP ROW: Histogram + Violin
        html.Div(
            style={
                "display": "flex",
                "gap": "10px",
                "marginBottom": "8px",
                "flexWrap": "wrap",
            },
            children=[
                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "350px",
                        "backgroundColor": "white",
                        "padding": "6px",
                        "borderRadius": "8px",
                    },
                    children=[
                        html.Div(
                            "Distribution of Airbnb Prices",
                            style={
                                "fontSize": "14px",
                                "margin": "0 0 2px 0",
                                "fontWeight": "600",
                                "color": "#333",
                            },
                        ),
                        dcc.Graph(
                            id="price_hist",
                            config={"scrollZoom": False},
                            style={"height": "240px"},
                        ),
                    ],
                ),
                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "350px",
                        "backgroundColor": "white",
                        "padding": "6px",
                        "borderRadius": "8px",
                    },
                    children=[
                        html.Div(
                            "Price by Neighbourhood Group",
                            style={
                                "fontSize": "14px",
                                "margin": "0 0 2px 0",
                                "fontWeight": "600",
                                "color": "#333",
                            },
                        ),
                        dcc.Graph(
                            id="price_violin",
                            config={"scrollZoom": False},
                            style={"height": "240px"},
                        ),
                    ],
                ),
            ],
        ),

        # BOTTOM: Map
        html.Div(
            style={
                "width": "100%",
                "backgroundColor": "white",
                "padding": "6px",
                "borderRadius": "8px",
                "marginBottom": "6px",
            },
            children=[
                html.Div(
                    "Geographic Distribution of Listings",
                    style={
                        "fontSize": "14px",
                        "margin": "0 0 2px 0",
                        "fontWeight": "600",
                        "color": "#333",
                    },
                ),
                dcc.Graph(
                    id="listing_map",
                    config={"scrollZoom": True},
                    style={"height": "260px"},
                ),
            ],
        ),
    ],
)

# ===========================
# Callback
# ===========================
@app.callback(
    Output("price_hist", "figure"),
    Output("price_violin", "figure"),
    Output("listing_map", "figure"),
    Output("kpi_avg_price", "children"),
    Output("kpi_num_listings", "children"),
    Output("kpi_avg_min_nights", "children"),
    Input("global_neigh_group", "value"),
    Input("global_room_type", "value"),
    Input("global_price_ceiling", "value"),
)
def update_all(neigh_group, room_type, price_ceiling):
    data = df.copy()

    if neigh_group != "All":
        data = data[data["neighbourhood_group"] == neigh_group]

    if room_type != "All":
        data = data[data["room_type"] == room_type]

    if price_ceiling != "none":
        data = data[data["price"] <= float(price_ceiling)]

    if data.empty:
        empty_fig = px.scatter(title="No data for selected filters")
        empty_fig.update_layout(
            xaxis={"visible": False},
            yaxis={"visible": False},
            template="simple_white",
            height=220,
        )
        return empty_fig, empty_fig, empty_fig, "N/A", "N/A", "N/A"

    avg_price = data["price"].mean()
    num_listings = len(data)
    avg_min_nights = data["minimum_nights"].mean()

    kpi_avg_price = f"${avg_price:,.0f}"
    kpi_num_listings = f"{num_listings:,}"
    kpi_avg_min_nights = f"{avg_min_nights:.1f} nights"

    # Histogram
    base_cap = 800
    if price_ceiling != "none":
        base_cap = min(base_cap, float(price_ceiling))
    hist_data = data[data["price"] <= base_cap]

    hist_fig = px.histogram(
        hist_data,
        x="price",
        color="neighbourhood_group",
        nbins=50,
        opacity=0.8,
        barmode="overlay",
        color_discrete_map=borough_colors,
    )
    hist_fig.update_layout(
        xaxis_title="Nightly Price (USD)",
        yaxis_title="Number of Listings",
        template="simple_white",
        height=220,
        margin=dict(l=40, r=5, t=10, b=30),
        legend_title="Neighbourhood Group",
        dragmode=False,
        hovermode="closest",
        showlegend=True,
    )
    hist_fig.update_xaxes(range=[0, base_cap], fixedrange=True)
    hist_fig.update_yaxes(fixedrange=True)

    # Violin + stats hover
    stats = (
        data.groupby("neighbourhood_group")["price"]
        .agg(
            min_price="min",
            q1_price=lambda s: s.quantile(0.25),
            median_price="median",
            q3_price=lambda s: s.quantile(0.75),
            max_price="max",
        )
        .reset_index()
    )
    data_violin = data.merge(stats, on="neighbourhood_group", how="left")

    violin_fig = px.violin(
        data_violin,
        x="neighbourhood_group",
        y="price",
        color="neighbourhood_group",
        box=True,
        points=False,
        color_discrete_map=borough_colors,
        category_orders={"neighbourhood_group": neigh_groups},
        custom_data=[
            "room_type",
            "minimum_nights",
            "number_of_reviews",
            "min_price",
            "q1_price",
            "median_price",
            "q3_price",
            "max_price",
        ],
    )
    violin_fig.update_layout(
        xaxis_title="Neighbourhood Group",
        yaxis_title="Nightly Price (USD)",
        template="simple_white",
        height=220,
        margin=dict(l=40, r=5, t=10, b=40),
        legend_title="Neighbourhood Group",
        dragmode=False,
        hovermode="closest",
        showlegend=True,
    )
    violin_fig.update_yaxes(range=[0, PRICE_AXIS_MAX], fixedrange=True)
    violin_fig.update_xaxes(tickangle=0)
    violin_fig.update_traces(
        hovertemplate=(
            "Neighbourhood: %{x}<br>"
            "Price: %{y:$,.0f}<br>"
            "Room type: %{customdata[0]}<br>"
            "Min nights: %{customdata[1]}<br>"
            "Reviews: %{customdata[2]}<br>"
            "<br>"
            "Group stats:<br>"
            "Min: %{customdata[3]:$,.0f}<br>"
            "Q1: %{customdata[4]:$,.0f}<br>"
            "Median: %{customdata[5]:$,.0f}<br>"
            "Q3: %{customdata[6]:$,.0f}<br>"
            "Max: %{customdata[7]:$,.0f}<extra></extra>"
        )
    )

    # Map
    map_data = data.dropna(subset=["latitude", "longitude"]).copy()
    map_fig = px.scatter_mapbox(
        map_data,
        lat="latitude",
        lon="longitude",
        color="neighbourhood_group",
        color_discrete_map=borough_colors,
        size="number_of_reviews",
        size_max=8,
        zoom=9.8,
        center={"lat": 40.7128, "lon": -74.0060},
        mapbox_style="carto-positron",
        hover_name="neighbourhood",
        hover_data={
            "price": True,
            "room_type": True,
            "number_of_reviews": True,
            "minimum_nights": True,
        },
    )
    map_fig.update_traces(marker={"opacity": 0.6})
    map_fig.update_layout(
        height=260,
        margin={"l": 0, "r": 0, "t": 10, "b": 0},
        paper_bgcolor="#FFFFFF",
        font={"family": "system-ui, -apple-system, 'Segoe UI', sans-serif", "size": 11},
        legend_title="Neighbourhood Group",
    )

    return (
        hist_fig,
        violin_fig,
        map_fig,
        kpi_avg_price,
        kpi_num_listings,
        kpi_avg_min_nights,
    )


if __name__ == "__main__":
    app.run(debug=True)
