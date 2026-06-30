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
from .input import ActivityFrequencyInput, AttributeInput, EventTypeSelection, ObjectTypeSelection
from .resource import ActivityDistribution, AttributePlot
from .util import activity_distribution, event_attributes_time, event_attribute_frequency, object_attribute_frequency





class OCELAnalysis(Plugin):  
    label = "OCEL Analysis"
    description = "A Plugin to analyze Object-Centric Event Logs"
    version = "1.0"

    @plugin_method(label="Iterations of Activities for Single Object Types", description="Analyze Iterations of Activities per Object Type")
    def activity_distribution_method(
        self,
        ocel: Annotated[OCEL, OCELAnnotation(label="Event Log")],
        input: ActivityFrequencyInput,
    ) -> ActivityDistribution:
        return activity_distribution(ocel, input)

    @plugin_method(label="Attribute Analysis", description="Analyze Event and Object Attribute Values over Time and Frequency")
    def event_attribute_values(
        self,
        ocel: Annotated[OCEL, OCELAnnotation(label="Event Log")],
        input: AttributeInput,
    ) -> AttributePlot:
        if isinstance(input.selection, EventTypeSelection):
            if input.selection.analysis_type == 'Time':
                return event_attributes_time(ocel, input)  
            elif input.selection.analysis_type == 'Frequency':
                return event_attribute_frequency(ocel,input)
            
        elif isinstance(input.selection, ObjectTypeSelection):
                return object_attribute_frequency(ocel, input)
        

