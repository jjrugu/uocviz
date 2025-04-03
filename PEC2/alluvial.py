import plotly.graph_objects as go
import pandas as pd
import seaborn as sns

df = pd.read_csv("data/data_sankey.csv", encoding="ISO-8859-1")
nodes = sorted(pd.unique(df[["source", "target"]].values.ravel()))
node_map = {node: idx for idx, node in enumerate(nodes)}
df["source_index"] = df["source"].map(node_map)
df["target_index"] = df["target"].map(node_map)
palette = sns.color_palette("tab20", len(nodes)).as_hex()
node_colors = [palette[i] for i in range(len(nodes))]
fig = go.Figure(
    data=[
        go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                # label=[df.columns[1:]],
                label=nodes,
                color=node_colors,
            ),
            link=dict(
                source=df["source_index"], target=df["target_index"], value=df["value"]
            ),
        )
    ]
)

fig.update_layout(
    title="Desglose de gastos destinados a COVID en 2021 en Dinamarca",
    title_x=0.5,
    title_xanchor="center",
    title_y=1,
    title_yanchor="top",
)
fig.write_image("output/sankey.png")
fig.show(renderer="browser")
