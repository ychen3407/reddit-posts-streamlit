import streamlit as st
from data_cleaning import *

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


st.html(
    "<h3>Posts Trend in TikTok Subreddit</h3>"
    )
# create time-series plot
df['date'] = df['timestamp'].dt.date
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
