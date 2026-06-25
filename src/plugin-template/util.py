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

    df_filtered = relation_df.loc[relation_df['ocel:type'] == input.object_type]
    object_activity_counts = (
        df_filtered.groupby(["ocel:oid", "ocel:activity"])
        .size()
        .reset_index(name="iterations")
    )
    object_activity_counts.rename(columns={
        "ocel:activity": "Activity",
        "iterations": "Execution No."
    },inplace=True)
    distribution = (
        object_activity_counts
        .groupby(["Activity", "Execution No."])
        .size()
        .reset_index(name="count")
    )

    x.relation_df = distribution.to_dict(orient='records')
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
    series = attribute_table[attribute_table["ocel:activity"] == input.event_type][input.event_attribute]

    nan_count = series.isna().sum()
    series = series.dropna()

    plot.event_type = input.event_type
    plot.event_attribute = input.event_attribute
    plot.analysis_type = input.analysis_type
    plot.nan_count = nan_count

    if pd.api.types.is_numeric_dtype(series):
        plot.data_type = "numerical"
        plot.attribute_table = [{input.event_attribute: float(v)} for v in series]

    else:
        plot.data_type = "categorical"
        counts = (series.value_counts().reset_index())
        counts.columns = [input.event_attribute, "Count"]
        plot.attribute_table = counts.to_dict(orient="records")

    return plot


    


