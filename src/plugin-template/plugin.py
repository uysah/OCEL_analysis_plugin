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
from .input import ActivityFrequencyInput
from .resource import ActivityDistribution
from .util import activity_distribution





class OCELAnalysis(Plugin):  # Rename me
    label = "OCEL Analysis"
    description = "A Plugin to analyze Object-Centric Event Logs"
    version = "0.1.0"

    @plugin_method(label="Activity Distribution per Object Type", description="Analyze Acitivity Frequencies per Object Type")
    def activity_distribution_method(
        self,
        ocel: Annotated[OCEL, OCELAnnotation(label="Event Log")],
        input: ActivityFrequencyInput,
    ) -> ActivityDistribution:
        return activity_distribution(ocel, input)

    @plugin_method(label="Activity Distribution per Object Type", description="Analyze Acitivity Frequencies per Object Type")
    def event_attribute_values(
        self,
        ocel: Annotated[OCEL, OCELAnnotation(label="Event Log")],
        input: Input,
    ) -> ActivityDistribution:
        return activity_distribution(ocel, input)  
