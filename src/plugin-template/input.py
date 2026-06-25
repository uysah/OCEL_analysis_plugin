from ocelescope import COMPUTED_SELECTION, OCEL, PluginInput, OCEL_FIELD
from typing import Literal
from pydantic import Field, BaseModel
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
#          Attributes
#========================================


class EventTypeSelection(BaseModel):
    class Config:
        title = "Event"
    
    selected_type: str = COMPUTED_SELECTION(
        title="Activity",
        provider='compute_event_types',
        depends_on=[],
    )
    event_attribute: str = COMPUTED_SELECTION(
        title="Attribute",
        provider='computed_event_attribute',
        depends_on=['selected_type'],
    )

class ObjectTypeSelection(BaseModel):
    class Config:
        title = "Object"
    
    selected_type: str = COMPUTED_SELECTION(
        title="Object Type",
        provider='compute_object_types',
        depends_on=[],
    )
    selected_activity: str = COMPUTED_SELECTION(
        title="Activity",
        provider='compute_selected_activity',
        depends_on=['selected_type'],
    )
    event_attribute: str = COMPUTED_SELECTION(
        title="Attribute",
        provider='computed_object_attribute',
        depends_on=['selected_type'],
    )

class AttributeInput(PluginInput):
    selection: EventTypeSelection | ObjectTypeSelection

    analysis_type: Literal['Time', 'Frequency'] = Field(
        title="Analysis Type",
        default='Frequency'
    )

    @staticmethod
    def compute_event_types(ocel: OCEL, input: dict):
        return ocel.events.df['ocel:activity'].unique().tolist()

    @staticmethod
    def compute_object_types(ocel: OCEL, input: dict):
        return ocel.objects.df['ocel:type'].unique().tolist()

    @staticmethod
    def compute_selected_activity(ocel: OCEL, input: dict):
        selected_type = input['selection']['selected_type']
        activitites = list(ocel.e2o.df[ocel.e2o.df['ocel:type'] == selected_type]['ocel:activity'].unique())
        return activitites
    @staticmethod
    def computed_event_attribute(ocel: OCEL, input: dict):
        print(input)
        selected_type = input['selection']['selected_type']
        if not selected_type:
            return []
        df = ocel.events.df[ocel.events.df['ocel:activity'] == selected_type]
        exclude = {'ocel:eid', 'ocel:activity', 'ocel:timestamp'}
        return [c for c in df.dropna(axis=1, how='all').columns if c not in exclude]

    @staticmethod
    def computed_object_attribute(ocel: OCEL, input: dict):
        selected_type = input['selection']['selected_type']
        if not selected_type:
            return []
        df = ocel.objects.df[ocel.objects.df['ocel:type'] == selected_type]
        exclude = {'ocel:oid', 'ocel:type', 'ocel:timestamp'}
        return [c for c in df.dropna(axis=1, how='all').columns if c not in exclude]