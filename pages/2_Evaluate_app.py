import streamlit as st

st.write("### Thank you for testing this app !")
st.write("#### Now give us your review.")
col1, col2 = st.columns(2)
col1.link_button(label="KoboToolbox", url="https://ee.kobotoolbox.org/x/btUWootj", width="stretch", type="primary")
col2.link_button(label="Google Forms", url="https://docs.google.com/forms/d/e/1FAIpQLSfRotBY5_94vd-5bH9LowLR_cbaUjsvWoeTtoQm1hNZoxGa_Q/viewform?usp=header", width="stretch")
