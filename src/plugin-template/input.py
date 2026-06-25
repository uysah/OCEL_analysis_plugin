from ocelescope import COMPUTED_SELECTION, OCEL, PluginInput, OCEL_FIELD
from typing import Literal
from pydantic import Field
#========================================
#          Activitiy Frequency
#========================================

class ActivityFrequencyInput(PluginInput):

    object_type: str = COMPUTED_SELECTION(
        provider="computed_object_types",
    )

    # object_id: str = COMPUTED_SELECTION(
    #     provider="computed_object_ids",
    #     depends_on=["object_type"]
    # )

    @staticmethod
    def computed_object_types(ocel: OCEL):
        return [str(object_type) for object_type in ocel.objects.types]

    # @staticmethod
    # def computed_object_ids(ocel: OCEL, input: dict):
    #     object_type = input.get("object_type")
    #     ids = ocel.objects.df.loc[ocel.objects.df["ocel:type"] == object_type,"ocel:oid"].tolist()
    #     return ["All"] + ids
    
#========================================
#          Event Attributes
#========================================




class EventAttribute(PluginInput):
    event_type: str = OCEL_FIELD(
        field_type="event_type",
        title="Event Type",
        ocel_id="ocel",
        description="The type of the event that should be analyzed",
    )

    event_attribute: str = COMPUTED_SELECTION(
        provider="computed_event_attribute",
        depends_on=["event_type"]
    )

    analysis_type: Literal['Time', 'Frequency'] = Field(title="Analysis Type", description="Analyze frequency or time behavior of event attributes", default='Time')

    @staticmethod
    def computed_event_attribute(ocel: OCEL, input:dict):
        event_type = input.get('event_type')
        attribute_table = ocel.events.df
        attribute_table = attribute_table[attribute_table['ocel:activity'] == event_type]
        event_attributes = [
            col for col in attribute_table.dropna(axis=1, how='all').columns.tolist()
            if col not in {'ocel:eid', 'ocel:activity', 'ocel:timestamp'}
        ]
        return event_attributes