import os

from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory, ConversationBufferWindowMemory
from langchain import OpenAI, ConversationChain
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent

os.environ["OPENAI_API_KEY"] = "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"
gpt_model = "gpt-4"

llm = ChatOpenAI(model_name=gpt_model, temperature=0.0)
llm = OpenAI(
    temperature=0,
    model_name=gpt_model
)


def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        print(f"Spent a total of {cb.total_tokens} tokens")
    return result


conversation = ConversationChain(
    llm=llm
)

print(conversation.prompt.template)

conversation_buf = ConversationChain(
    llm=llm,
    memory=ConversationBufferMemory()
)

print(conversation_buf("good morning. AI!"))
print(count_tokens(
    conversation_buf,
    "My aim here is to explore how to become expert of cybersecurity."
))
# print(conversation_buf.run("My aim here is to explore how to become expert of cybersecurity.")) # they are the same
print(count_tokens(
    conversation_buf,
    "I am also learning some skills and knowledge of Machine Learning. What should I do to become an expert in this area?."
))
print(count_tokens(
    conversation_buf,
    "As the career I mentioned before.I want to take full use of my advantages.How to combine those two skills together?"
))

print(conversation_buf.memory.buffer)


# in order to have a higher reading and understanding, gpt should not take all the history before.
# but just some summary of it.

conversation_sum = ConversationChain(
    llm=llm,
    memory=ConversationSummaryMemory(llm=llm)
)
print(conversation_sum.memory.prompt.template)

print(conversation_sum("good morning. AI!"))
print(count_tokens(
    conversation_sum,
    "My aim here is to explore how to become expert of cybersecurity."
))
print(count_tokens(
    conversation_sum,
    "I am also learning some skills and knowledge of Machine Learning. What should I do to become an expert in this area?."
))
print(count_tokens(
    conversation_sum,
    "As the career I mentioned before.I want to take full use of my advantages.How to combine those two skills together?"
))

print(conversation_sum.memory.buffer) # so it takes less buffer in context. also->create a list to store memory could store more information


# Memory Type3 :
conversation_bufw = ConversationChain(
    llm=llm,
    memory=ConversationBufferWindowMemory(k=1)
)
print(conversation_bufw("good morning. AI!"))
print(count_tokens(
    conversation_bufw,
    "My aim here is to explore how to become expert of cybersecurity."
))

