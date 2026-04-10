from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat = ChatPromptTemplate([
    ('system','You are an helpful assistant'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human','{query}')
])

chat_history = []

with open('4_Prompts/chat_hist.txt') as f:
    chat_history.extend(f.readlines())

print(chat_history)

prompt = chat.invoke({'chat_history':chat_history,'query':"When i will get"})

print(prompt)