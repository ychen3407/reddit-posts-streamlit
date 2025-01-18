import streamlit as st
from data_cleaning import *

st.title("Some Facts :thinking_face:")

kw_extractor = get_kw_extractor()
path = 'subreddit_2025-01-17.json'
df = clean(path, extractor=kw_extractor)

n = st.number_input(
    "Pick a int from 1 to 10 for upvoted/downvoted posts",
    min_value = 1, 
    max_value = 10,
    step = 1)

option = st.selectbox(
    "What would you like to see?",
    ("most upvoted", 
     "least upvoted", 
     "most commented", 
     "most votes",
     "most controversial"),
)


cols = ['timestamp', 'title', 'ups', 'selftext']

new_df = None
if option == 'most upvoted':
    # top n upvoted posts
    new_df = df.sort_values(by='ups', ascending=False)[cols].head(n)
elif option == 'least upvoted':
    pass
elif option == 'most commented':
    new_df = df.sort_values(by='num_comments', ascending=False)[cols].head(n)
elif option == 'most votes':
    pass
else:
    new_df = df[df['upvote_ratio'].between(0.4, 0.6)]

st.dataframe(new_df)
st.write(
    "Note: controverial post is defined as upvote ratio around .5"
)