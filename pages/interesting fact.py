import streamlit as st
from data_cleaning import *

st.title("Some Facts :thinking_face:")

kw_extractor = get_kw_extractor()
path = 'subreddit_2025-01-17.json'
df = clean(path, extractor=kw_extractor)

# calculate total votes and downvotes
df['total_votes'] = (df['ups']/df['upvote_ratio']).astype(int)
df['down_votes'] = df['total_votes'] - df['ups']

n = st.number_input(
    "Select num of posts you want to see (1-10)",
    min_value = 1, 
    max_value = 10,
    step = 1)

option = st.selectbox(
    "What would you like to see?",
    ("most upvoted", 
     "most downvoted", 
     "most commented", 
     "most votes",
     "most controversial"),
)


cols = ['timestamp', 'title', 'selftext']

new_df = None
if option == 'most upvoted':
    # top n upvoted posts
    new_df = df.sort_values(by='ups', ascending=False)[cols].head(n)
elif option == 'most downvoted':
    new_df = df.sort_values(by='down_votes', ascending=False)[cols].head(n)
elif option == 'most commented':
    new_df = df.sort_values(by='num_comments', ascending=False)[cols].head(n)
elif option == 'most votes':
    new_df = df.sort_values(by='total_votes', ascending=False)[cols].head(n)
else:
    new_df = df[df['upvote_ratio'].between(0.4, 0.6)][cols].head(n)

st.dataframe(new_df)
st.write(
    "Note: controverial post is defined as upvote ratio around .5"
)