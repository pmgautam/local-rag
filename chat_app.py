import streamlit as st

from src.vector_db import VectorDB


@st.cache_resource
def init_vector_db():
    return VectorDB()


class ChatbotUI:
    def __init__(self):
        self.vector_db = init_vector_db()
        self.collections = self.vector_db.list_collections()

    def initialize_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "selected_collection" not in st.session_state:
            st.session_state.selected_collection = self.collections[0]

    def handle_user_input(self) -> None:
        prompt = st.chat_input("What is your question?")
        if prompt:
            with st.chat_message("user"):
                st.write(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            self.generate_assistant_response(prompt)

    def generate_assistant_response(self, prompt) -> None:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            full_response = ""
            for chunk in self.vector_db.query(
                prompt, collection_name=st.session_state.selected_collection
            ):
                content = chunk["message"]["content"]
                full_response += content
                message_placeholder.markdown(full_response + " ▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

    def display_collection_dropdown(self):
        new_collection = st.selectbox(
            "Select a collection:",
            options=self.collections,
            index=self.collections.index(st.session_state.selected_collection),
            key="collection_dropdown",
        )
        if new_collection != st.session_state.selected_collection:
            st.session_state.selected_collection = new_collection
            # st.session_state.messages = []  # Clear message history when changing collection
            # st.rerun()

    def display_chat_history(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


def main() -> None:
    st.title("RAG Chatbot")
    ui = ChatbotUI()
    ui.initialize_session_state()
    ui.display_collection_dropdown()
    ui.display_chat_history()
    ui.handle_user_input()


if __name__ == "__main__":
    main()
