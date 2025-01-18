import streamlit as st
from data_cleaning import *

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.title(":grin: Sentiment Analysis :weary:")
st.sidebar.markdown("# Sentiment Analysis :smile: :cold_sweat:")

# TODO: find a better way to read data
kw_extractor = get_kw_extractor()
path = 'subreddit_2025-01-17.json'
df = clean(path, extractor=kw_extractor)

df['date'] = df['timestamp'].dt.date


# sentiment pct
st.html(
    "<h3>Overall Sentiment Precentage</h3>"
)
agg_sentiment_df = df[['sentiment']].groupby('sentiment').size().reset_index()
agg_sentiment_df = agg_sentiment_df.rename(columns={0: 'cnt'})

fig = go.Figure(data=[go.Pie(labels=agg_sentiment_df['sentiment'],
                             values=agg_sentiment_df['cnt'])])
fig.update_traces(hoverinfo='label+value', textinfo='percent', textfont_size=20,
                  marker=dict(colors=['#87CEFA', '#000080', '#FFC0CB'], line=dict(color='white', width=2)))
st.plotly_chart(fig)

# sentiment trend over time
st.html(
    "<h3>How are people feeling over time...</h3>"
)
agg_df = df.groupby(['date', 'sentiment']).size().reset_index()
agg_df = agg_df.rename(columns = {0: 'cnt'})
st.line_chart(agg_df, 
              x='date', 
              y='cnt', 
              color='sentiment',
              y_label='# of posts')


# processing key words
st.html(
    """
    <h3>Some keywords analysis...</h3>
    <p>The following section tries to capture people's feelings on certain aspects.
    e.g. recent TikTok ban
    </p>
    """
)


def replace_kw(kw):
  """
  This function is meant to provide a simple and basic method to cluster some
  common keywords, not comprehensive, can be adjusted, e.g. comment out the last of
  code will also help us to filter out desired keywords
  """
  if pd.isna(kw):
    return None
  if 'ban' in kw:
    return 'ban'
  if 'rednote' in kw or 'red note' in kw or 'xihongshu' in kw or 'red book' in kw:
    return 'rednote'
  if 'data' in kw:
    return 'data'
  if 'tik' in kw or 'tok' in kw:
    return 'tiktok'
  # return kw


df['all_keywords'] = df['title_kw'] + df['text_kw']
kw_df = df.explode(column=['all_keywords'])[['all_keywords', 'sentiment']]
kw_df['all_keywords']=kw_df['all_keywords'].str.lower()

kw_df['all_keywords'] = kw_df['all_keywords'].apply(replace_kw)
agg_kw_sentiment_df = kw_df.dropna().groupby(['all_keywords', 'sentiment']).size().reset_index()
agg_kw_sentiment_df = agg_kw_sentiment_df.rename(columns={0: 'cnt'})

st.bar_chart(agg_kw_sentiment_df, 
             x="all_keywords", 
             y="cnt", 
             x_label='keyword',
             y_label='pct of posts',
             color="sentiment", 
             horizontal=True,
             stack='normalize')