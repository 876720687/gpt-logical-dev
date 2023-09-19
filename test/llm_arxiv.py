import os

from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

os.environ["OPENAI_API_KEY"] = "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"


llm = ChatOpenAI(temperature=0.0)
# tools = load_tools(
#     ["arxiv"],
# )

# agent_chain = initialize_agent(
#     tools,
#     llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True,
# )

memory = ConversationBufferMemory(memory_key="history", return_messages=True)

chain = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True)

chain.run("""
    "What's the paper https://arxiv.org/abs/1706.03762 about?"
"""
)