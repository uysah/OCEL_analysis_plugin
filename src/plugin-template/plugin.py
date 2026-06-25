from typing import Annotated

from ocelescope import (
    OCEL,
    OCELAnnotation,
    Plugin,
    PluginInput,
    Resource,
    plugin_method,
    Table,
    TableColumn
)
from .input import ActivityFrequencyInput, EventAttribute
from .resource import ActivityDistribution, EventAttributePlot
from .util import activity_distribution, event_attributes_time, event_attribute_frequency





class OCELAnalysis(Plugin):  
    label = "OCEL Analysis"
    description = "A Plugin to analyze Object-Centric Event Logs"
    version = "0.1.0"

    @plugin_method(label="Iterations of Activities for Single Object Types", description="Analyze Acitivity Frequencies per Object Type")
    def activity_distribution_method(
        self,
        ocel: Annotated[OCEL, OCELAnnotation(label="Event Log")],
        input: ActivityFrequencyInput,
    ) -> ActivityDistribution:
        return activity_distribution(ocel, input)

    @plugin_method(label="Event Attribute Analysis", description="Analyze Event Attribute Values over time")
    def event_attribute_values(
        self,
        ocel: Annotated[OCEL, OCELAnnotation(label="Event Log")],
        input: EventAttribute,
    ) -> EventAttributePlot:
        if input.analysis_type == 'Time':
            return event_attributes_time(ocel, input)  
        elif input.analysis_type == 'Frequency':
            return event_attribute_frequency(ocel,input)

