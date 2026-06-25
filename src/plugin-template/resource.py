from ocelescope import Resource,Table, TableColumn
from ocelescope.visualization.default.plotly import Plotly
import plotly.express as px
import numpy as np
import pandas as pd

#========================================
#          Activitiy Frequency
#========================================

CHART_COLOURS = [
    "#006165", "#CE108A", "#0098A1", "#F6A800",
    "#00549F", "#6f2b4b", "#8EBAE5", "#000080",
    "#007e56", "#005d4c", "#a1dfd7", "#cd00cd",
    "#28713e", "#701f29", "#5d2141", "#a1dfd7",
    "#00ffff", "#39ff14", "#800080", "#005f6a",
    "#76e1e0", "#f5ff00",
]


class ActivityDistribution(Resource):
    label = "Stacked Bar Chart"
    description = "Activity Distribution per Object Type"

    object_type: str = ''
    object_id: str = ''
    relation_df: list[dict] = []

    def color_map(self,strings: list[str]) -> dict[str, str]:
            unique = sorted(set(strings), key=lambda x: int(x))

            return {
                value: CHART_COLOURS[i % len(CHART_COLOURS)]
                for i, value in enumerate(unique)
        }

    def visualize(self) -> Table:
        df = pd.DataFrame(self.relation_df)
        unique_iterations = sorted(df["Execution No."].unique(),key=int)
        color_map = self.color_map(unique_iterations)
        df["Execution No."] = df["Execution No."].astype(str)

        fig = px.bar(
            df,
            x="Activity",
            y="count",
            color="Execution No.",
            barmode="stack",
            color_discrete_map=color_map,
            title=f"Iteration of Activities for {self.object_type}",
            labels={
                "count": "Count",
                "Execution No.": "Iterations",
                "Activity": "Activity"
            }
        )

        return Plotly(figure=fig)
     
#========================================
#               Attribute 
#========================================


class AttributePlot(Resource):
    label = "Line and Bar Chart"
    description = 'Time Analysis of Event Attribute Values'

    event_type: str = ''
    event_attribute: str = ''
    attribute_table: list[dict] = []
    analysis_type: str = ''
    data_type: str = ''
    nan_count: int = 0

    def visualize(self)-> Plotly:
        if self.analysis_type == 'Time':
            fig = px.line(
                self.attribute_table,
                x="Timestamp",
                y="Value",
                title=f"Time Analysis of Attribute Values of {self.event_attribute} for Event Type {self.event_type}",
            )

        elif self.analysis_type == "Frequency":
                    df = pd.DataFrame(self.attribute_table)
                    if self.nan_count > 0:
                        nan_row = pd.DataFrame([{self.event_attribute: "NaN", "Count": self.nan_count}])
                        df = pd.concat([df, nan_row], ignore_index=True)
                    if self.data_type == "categorical":
                        fig = px.bar(
                            df,
                            x=self.event_attribute,
                            y="Count",
                            title=(
                                f"Attribute Value Distribution of {self.event_attribute} "
                                f"for Event Type {self.event_type}"
                            ),
                        )

                    elif self.data_type == "numerical":
                        values = df[self.event_attribute].astype(float)
                        
                        unique_vals = values.nunique()
                        val_range = values.max() - values.min()

                        if unique_vals == 1 or val_range == 0:
                            fig = px.bar(
                                x=[str(values.iloc[0])],
                                y=[len(values)],
                                labels={"x": self.event_attribute, "y": "Count"},
                                title=f"Attribute Value Distribution of {self.event_attribute} for Event Type {self.event_type} (all values identical)",
                            )
                        else:
                            n = len(values)
                            q25, q75 = np.percentile(values, [25, 75])
                            iqr = q75 - q25

                            if iqr > 0:
                                bin_width = 2 * iqr / (n ** (1 / 3))
                                nbins = max(1, int(np.ceil(val_range / bin_width)))
                            else:
                                nbins = int(np.ceil(np.log2(n) + 1))

                            bin_size = val_range / nbins if nbins > 0 else val_range
                            fig = px.histogram(
                                df, x=self.event_attribute,
                                title=f"Attribute Value Distribution of {self.event_attribute} for {self.event_type}",
                            )
                            fig.update_traces(xbins=dict(
                                start=float(values.min()),
                                end=float(values.max()),
                                size=bin_size,
                            ))
        return Plotly(figure=fig)
            

