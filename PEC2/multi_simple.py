import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv("data/consumption_monthly.csv", delimiter=";")
df["date"] = pd.to_datetime(df["Month"])
df["M"] = df["date"].dt.month
df["Y"] = df["date"].dt.year
df["ConsumptiongWh"] = (
    df["ConsumptionkWh"].str.replace(",", ".").astype(dtype=float) / 1000000.0
).round(2)
types = pd.unique(df["Branche"])
years = pd.unique(df["Y"])
fig = make_subplots(
    rows=len(years),
    cols=len(types),
    vertical_spacing=0.09,
    horizontal_spacing=0.11,
)

colors = ["#A3C4DC", "#F6B7B7", "#B9E2A2"]
annotations = []
for i, y in enumerate(pd.unique(df["Y"].sort_values())):
    for j, t in enumerate(pd.unique(types)):
        consumption = df[(df["Branche"] == t) & (df["Y"] == y)][
            ["M", "ConsumptiongWh"]
        ].sort_values(by="M")
        fig.add_trace(
            go.Bar(
                x=consumption["M"],
                y=consumption["ConsumptiongWh"],
                marker=dict(color=colors[j]),
                showlegend=False,
            ),
            row=i + 1,
            col=j + 1,
        )
    annotations.append(
        dict(
            text=f"{y}",
            x=1.1,
            y=0.95 - (i * 0.3),
            showarrow=False,
            font=dict(size=14),
            xref="paper",
            yref="paper",
        )
    )
annotations.extend(
    [
        dict(
            text="Industria",
            x=0.10,
            y=1.1,
            showarrow=False,
            font=dict(size=14),
            xref="paper",
            yref="paper",
        ),
        dict(
            text="Público",
            x=0.5,
            y=1.1,
            showarrow=False,
            font=dict(size=14),
            xref="paper",
            yref="paper",
        ),
        dict(
            text="Privado",
            x=0.90,
            y=1.1,
            showarrow=False,
            font=dict(size=14),
            xref="paper",
            yref="paper",
        ),
    ]
)

fig.update_layout(
    annotations=annotations,
    title="Consumo en GWh entre 2021-2024 para los sectores industria, público y privado en Copenhagen",
    title_x=0.5,
    title_xanchor="center",
    title_y=1,
    title_yanchor="top",
)
fig.update_xaxes(title_text="Mes")
fig.update_yaxes(title_text="GWh")
fig.write_image("output/multi.png")
fig.show(renderer="browser")
