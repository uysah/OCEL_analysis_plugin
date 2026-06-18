from ocelescope import OCEL
from .input import ActivityFrequencyInput, EventAttribute
from .resource import ActivityDistribution, EventAttributePlot
import numpy as np
import pandas as pd
#========================================
#          Activitiy Frequency
#========================================

def activity_distribution(ocel:OCEL, input: ActivityFrequencyInput) -> ActivityDistribution:
    x = ActivityDistribution()
    x.object_type = input.object_type
    relation_df = ocel.e2o.df

    if input.object_id == 'All':
        df_filtered = relation_df.loc[relation_df['ocel:type'] == input.object_type]
        counts = df_filtered['ocel:activity'].value_counts().reset_index()
        counts.columns = ['Activity', 'Count']
    else:
        df_filtered = relation_df.loc[(relation_df['ocel:type'] == x.object_type) & (relation_df['ocel:oid'] == input.object_id)]
        counts = df_filtered['ocel:activity'].value_counts().reset_index()
        counts.columns = ['Activity', 'Count']
        x.object_id == input.object_id

    x.relation_df = counts.to_dict(orient='records')
    return x


#========================================
#          Event Attribute 
#========================================

def event_attributes_time(ocel:OCEL,input: EventAttribute) -> EventAttributePlot:
    plot = EventAttributePlot()
    attribute_table = ocel.events.df
    data_df = attribute_table[attribute_table['ocel:activity'] == input.event_type][[input.event_attribute,'ocel:timestamp']]
    data_df.rename(columns=
        {
            "ocel:timestamp": "Timestamp",
            input.event_attribute: "Value"
        },inplace=True
    )

    plot.event_type = input.event_type
    plot.event_attribute = input.event_attribute
    plot.attribute_table = data_df.to_dict(orient='records')
    plot.analysis_type = input.analysis_type
    return plot

def event_attribute_frequency(ocel:OCEL,input: EventAttribute) -> EventAttributePlot:
    plot = EventAttributePlot()
    attribute_table = ocel.events.df
    series = (attribute_table[attribute_table["ocel:activity"] == input.event_type][input.event_attribute].dropna())

    plot.event_type = input.event_type
    plot.event_attribute = input.event_attribute
    plot.analysis_type = input.analysis_type

    if pd.api.types.is_numeric_dtype(series):
        plot.data_type = "continuous"
        plot.attribute_table = [{input.event_attribute: float(v)} for v in series]

    else:
        plot.data_type = "categorical"
        counts = (series.value_counts().reset_index())
        counts.columns = [input.event_attribute, "Count"]
        plot.attribute_table = counts.to_dict(orient="records")

    return plot


    


