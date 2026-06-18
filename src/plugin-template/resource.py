from ocelescope import Resource,Table, TableColumn
from ocelescope.visualization.default.plotly import Plotly
import plotly.express as px
import numpy as np
import pandas as pd

#========================================
#          Activitiy Frequency
#========================================


class ActivityDistribution(Resource):
    label = "Bar Chart"
    description = "Activity Distribution per Object Type"

    object_type: str = ''
    object_id: str = ''
    relation_df: list[dict] = []

    def visualize(self) -> Table:
        fig = px.bar(
            self.relation_df,
            x="Activity",
            y="Count",
            color="Activity",
            title=f"Activity Distribution for Object Type {self.object_type}" + (f"for Object ID {self.object_id}" if self.object_id != '' else ""
        ))
        fig.update_layout(showlegend=False) 
        return Plotly(figure=fig)
     
#========================================
#          Event Attribute 
#========================================


class EventAttributePlot(Resource):
    label = "Line Chart"
    description = 'Time Analysis of Event Attribute Values'

    event_type: str = ''
    event_attribute: str = ''
    attribute_table: list[dict] = []
    analysis_type: str = ''
    data_type: str = ''

    def visualize(self)-> Plotly:
        if self.analysis_type == 'Time':
            fig = px.line(
                self.attribute_table,
                x="Timestamp",
                y="Value",
                title=f"Time Analysis of Event Attribute {self.event_attribute} Values for Event Type {self.event_type}",
            )

        elif self.analysis_type == "Frequency":
                    if self.data_type == "categorical":
                        df = pd.DataFrame(self.attribute_table)
                        fig = px.bar(
                            df,
                            x=self.event_attribute,
                            y="Count",
                            title=(
                                f"Frequency of {self.event_attribute} "
                                f"for Event Type {self.event_type}"
                            ),
                        )

                    elif self.data_type == "continuous":

                        df = pd.DataFrame(self.attribute_table)
                        values = df[self.event_attribute].astype(float)
                        n = len(values)
                        if n <= 1:
                            nbins = 1
                        else:
                            q25, q75 = np.percentile(values, [25, 75])
                            iqr = q75 - q25
                            if iqr > 0:
                                bin_width = 2 * iqr / (n ** (1 / 3))
                                nbins = max(1, int(np.ceil((values.max() - values.min()) / bin_width)))
                            else:
                                nbins = int(np.ceil(np.log2(n) + 1))

                        fig = px.histogram(
                            df,
                            x=self.event_attribute,
                            nbins=nbins,
                            title=f"Distribution of {self.event_attribute}"
                        )

        return Plotly(figure=fig)
            

