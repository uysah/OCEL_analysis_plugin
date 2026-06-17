from ocelescope import COMPUTED_SELECTION, OCEL, PluginInput


#========================================
#          Activitiy Frequency
#========================================

class ActivityFrequencyInput(PluginInput):

    object_type: str = COMPUTED_SELECTION(
        provider="computed_object_types",
    )

    object_id: str = COMPUTED_SELECTION(
        provider="computed_object_ids",
        depends_on=["object_type"],
        default=None,
    )

    @staticmethod
    def computed_object_types(ocel: OCEL):
        return [str(object_type) for object_type in ocel.objects.types]

    @staticmethod
    def computed_object_ids(ocel: OCEL, input: dict):
        object_type = input.get("object_type")
        if not object_type:
            return ["All"]

        ids = ocel.objects.df.loc[ocel.objects.df["ocel:type"] == object_type,"ocel:oid"].tolist()

        return ["All"] + ids
    
#========================================
#          Event Attributes
#========================================