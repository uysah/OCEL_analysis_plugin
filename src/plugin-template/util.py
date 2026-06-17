from ocelescope import OCEL
from .input import ActivityFrequencyInput
from .resource import ActivityDistribution

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