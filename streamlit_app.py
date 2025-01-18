import streamlit as st
from data_cleaning import *
import datetime

from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.title("🎈 Reddit Posts Analysis - TikTok Subreddit")
st.subheader(
    "Overview",
    divider='gray'
)

st.write("Built to analyze and visualize people's opinion of TikTok on :red[Reddit]")
st.sidebar.markdown("# Main page 🎈")

kw_extractor = get_kw_extractor()
path = 'subreddit_2025-01-17.json'
df = clean(path, extractor=kw_extractor)

# additional cleaning/transformation
df['date'] = df['timestamp'].dt.date


# set date range selector
today = datetime.datetime.now()
last_year = today.year - 1
jan_1 = datetime.date(last_year, 1, 1)
dec_31 = datetime.date(today.year, 12, 31)

d = st.date_input(
    "Select the date range you want to see (working on this feature...)",
    (jan_1, datetime.date(today.year, 1, 7)),
    jan_1,
    dec_31,
    format="MM.DD.YYYY",
)

# Given d=(start_date, end_date), filter df to this specific range
# start_date, end_date = d
# df_filtered = df[(df['date'] >= start_date) & (df['date'] < end_date)]


# post trend
st.html(
    "<h3>Posts Trend in TikTok Subreddit</h3>"
    )
# create time-series plot
st.line_chart(df.groupby('date').size(),
              x_label = 'date',
              y_label = '# of reddit posts',
              color = '#FF5700')


# create wordcloud plot
st.html(
    "<h3>Most Frequent Words in Posts</h3>"
)
wordcloud_text = ' '.join(df['selftext'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(wordcloud_text)
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')

st.pyplot(fig)


# create table view
st.html(
    "<h3>Example Data:</h3>"
    )

example_df = df[['timestamp', 'id', 'title', 'num_comments', 'ups', 'is_video', 'selftext']].copy()
st.dataframe(example_df.head(5))