from ocelescope import OCEL
from .input import ActivityFrequencyInput, AttributeInput
from .resource import ActivityDistribution, AttributePlot
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
#              Attribute 
#========================================

def event_attributes_time(ocel:OCEL,input: AttributeInput) -> AttributePlot:
    plot = AttributePlot()
    attribute_table = ocel.events.df
    event_type = input.selection.selected_type
    event_attribute = input.selection.event_attribute
    data_df = attribute_table[attribute_table['ocel:activity'] == event_type][[event_attribute,'ocel:timestamp']]
    data_df.rename(columns=
        {
            "ocel:timestamp": "Timestamp",
            event_attribute: "Value"
        },inplace=True
    )

    plot.event_type = event_type
    plot.event_attribute = event_attribute
    plot.attribute_table = data_df.to_dict(orient='records')
    plot.analysis_type = input.selection.analysis_type
    return plot

def event_attribute_frequency(ocel:OCEL,input: AttributeInput) -> AttributePlot:
    plot = AttributePlot()
    attribute_table = ocel.events.df
    event_type = input.selection.selected_type
    event_attribute = input.selection.event_attribute
    series = attribute_table[attribute_table["ocel:activity"] == event_type][event_attribute]

    nan_count = series.isna().sum()
    series = series.dropna()

    plot.event_type = event_type
    plot.event_attribute = event_attribute
    plot.analysis_type = input.selection.analysis_type
    plot.nan_count = nan_count

    if pd.api.types.is_numeric_dtype(series):
        plot.data_type = "numerical"
        plot.attribute_table = [{event_attribute: float(v)} for v in series]

    else:
        plot.data_type = "categorical"
        counts = (series.value_counts().reset_index())
        counts.columns = [event_attribute, "Count"]
        plot.attribute_table = counts.to_dict(orient="records")

    return plot

def object_attribute_frequency(ocel: OCEL, input: AttributeInput) -> AttributePlot:
    plot = AttributePlot()
    object_type = input.selection.selected_type
    activity = input.selection.selected_activity
    object_attribute = input.selection.event_attribute

    e2o = ocel.e2o.df
    relevant_e2o = e2o[(e2o["ocel:type"] == object_type) & (e2o["ocel:activity"] == activity)][["ocel:eid", "ocel:oid"]]
    obj_df = ocel.objects.df[ocel.objects.df["ocel:type"] == object_type][["ocel:oid", object_attribute]]
    merged = relevant_e2o.merge(obj_df, on="ocel:oid", how="left")

    series = merged[object_attribute]
    nan_count = int(series.isna().sum())
    series = series.dropna()

    plot.object_type = object_type
    plot.selected_activity = activity
    plot.event_attribute = object_attribute
    plot.analysis_type = "Frequency"
    plot.nan_count = nan_count

    if pd.api.types.is_numeric_dtype(series):
        plot.data_type = "numerical"
        plot.attribute_table = [{object_attribute: float(v)} for v in series]
    else:
        plot.data_type = "categorical"
        counts = series.value_counts().reset_index()
        counts.columns = [object_attribute, "Count"]
        plot.attribute_table = counts.to_dict(orient="records")

    return plot


