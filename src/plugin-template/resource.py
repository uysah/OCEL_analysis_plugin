from ocelescope import Resource,Table, TableColumn
from ocelescope.visualization.default.plotly import Plotly
import plotly.express as px

#========================================
#          Activitiy Frequency
#========================================


class ActivityDistribution(Resource):
    label = "Minimal Resource"
    description = "A minimal resource"

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
