"""Streamlit view. Keep it thin: load state, call poll.core, render."""

from datetime import datetime

import pandas as pd
import streamlit as st

from poll import store
from poll.core import create_poll, created_label, tally, total_votes, vote

st.set_page_config(page_title="Live Poll", page_icon="🗳️")
st.title("🗳️ Live Poll")

poll = store.load()

if poll is None:
    st.subheader("Create a poll")
    with st.form("create"):
        question = st.text_input("Question")
        options_text = st.text_area("Options, one per line")
        submitted = st.form_submit_button("Create poll")
    if submitted:
        try:
            store.save(create_poll(question, options_text.splitlines(), datetime.now()))
        except ValueError as err:
            st.error(str(err))
        else:
            st.rerun()
    st.stop()

st.subheader(poll["question"])
if label := created_label(poll):
    st.caption(label)

with st.form("vote"):
    choice = st.radio("Your vote", poll["options"])
    if st.form_submit_button("Vote"):
        store.save(vote(poll, choice))
        st.rerun()

results = pd.DataFrame(tally(poll), columns=["Option", "Votes"]).set_index("Option")
st.bar_chart(results)
st.caption(f"{total_votes(poll)} votes so far")

if st.button("Reset poll"):
    store.clear()
    st.rerun()
