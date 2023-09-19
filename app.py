import streamlit as st

from ethan.ethan_agent import EthanAgent

ethanAgent = EthanAgent()

st.title("💬 Ethan SQL Assistant")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant",
         "content": """Hi, I'm Ethan, a SQL assistant.
        I'm here to help you query and generate reports on your Music Database.
        How can I help you?
         """}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = ethanAgent.run(prompt, st.session_state["messages"])
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
