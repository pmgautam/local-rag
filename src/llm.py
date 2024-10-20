import ollama


def get_streaming_response(messages, stream=True):
    return ollama.chat(model="llama3.1", messages=messages, stream=stream)
