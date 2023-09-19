#!/usr/bin/env python
# coding: utf-8

# 引入包
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import UnstructuredFileLoader, DirectoryLoader
from pkg.models import ChatGLM
import sentence_transformers
import torch
import os

# 全局参数
EMBEDDING_MODEL = "text2vec" # embedding 模型，对应 embedding_model_dict
VECTOR_SEARCH_TOP_K = 6
LLM_MODEL = "chatglm-6b"     # LLM 模型名，对应 llm_model_dict
LLM_HISTORY_LEN = 3
DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec": "/home/mw/input/text2vec2538",
}

llm_model_dict = {
    "chatglm-6b-int4-qe": "THUDM/chatglm-6b-int4-qe",
    "chatglm-6b-int4": "THUDM/chatglm-6b-int4",
    "chatglm-6b": "/home/mw/input/ChatGLM6B6449",
}



# 初始化配置
def init_cfg(LLM_MODEL, EMBEDDING_MODEL, LLM_HISTORY_LEN, V_SEARCH_TOP_K=6):
    global chatglm, embeddings, VECTOR_SEARCH_TOP_K
    VECTOR_SEARCH_TOP_K = V_SEARCH_TOP_K

    chatglm = ChatGLM()
    chatglm.load_model(model_name_or_path=llm_model_dict[LLM_MODEL])
    chatglm.history_len = LLM_HISTORY_LEN

    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_dict[EMBEDDING_MODEL],)
    embeddings.client = sentence_transformers.SentenceTransformer(embeddings.model_name,
                                                                  device=DEVICE)


# In[10]:


# 初始化指定知识库的 vector_store
def init_knowledge_vector_store(filepath:str):
    docs = []
    if not os.path.exists(filepath):
        print("路径不存在")
        return None
    elif os.path.isfile(filepath):
        file = os.path.split(filepath)[-1]
        try:
            loader = UnstructuredFileLoader(filepath, mode="elements")
            docs = loader.load()
            print(f"{file} 已成功加载")
        except:
            print(f"{file} 未能成功加载")
            return None
    elif os.path.isdir(filepath):
        try:
            loader = DirectoryLoader(filepath, glob="**/*.md")
            docs = loader.load()
            print(f"{filepath} 已成功加载")
        except Exception as e:
            print(f"{filepath} 未能成功加载: {e}")
            return None

    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store


# In[11]:


# 结合知识库进行问题回答
def get_knowledge_based_answer(query, vector_store, chat_history=[]):
    global chatglm, embeddings

    prompt_template = """基于以下已知信息，简洁和专业的来回答用户的问题。
如果无法从中得到答案，请说 "根据已知信息无法回答该问题" 或 "没有提供足够的相关信息"，不允许在答案中添加编造成分，答案请使用中文。
已知内容:
{context}
问题:
{question}"""
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    chatglm.history = chat_history
    knowledge_chain = RetrievalQA.from_llm(
        llm=chatglm,
        retriever=vector_store.as_retriever(search_kwargs={"k": VECTOR_SEARCH_TOP_K}),
        prompt=prompt
    )
    knowledge_chain.combine_documents_chain.document_prompt = PromptTemplate(
            input_variables=["page_content"], template="{page_content}"
        )

    knowledge_chain.return_source_documents = True

    result = knowledge_chain({"query": query})
    chatglm.history[-1][0] = query
    return result, chatglm.history


# In[12]:


# 使用 Markdown 格式打印模型输出
from IPython.display import display, Markdown


def display_answer(query, vector_store, history = []):
    resp, history = get_knowledge_based_answer(query=query,
                                               vector_store=vector_store,
                                               chat_history=history)
    display(Markdown(resp["result"]))
    #return resp, history


# In[15]:


# 执行初始化
init_cfg(LLM_MODEL, EMBEDDING_MODEL, LLM_HISTORY_LEN)
vector_store = init_knowledge_vector_store("/home/mw/temp/d2l-zh-pytorch-2.0.0.pdf")#/home/mw/temp/book


# In[18]:


# 效果测试展示


# In[16]:


display_answer(query="ModelWhale 是什么",
                           vector_store=vector_store)


# In[19]:


display_answer(query="ModelWhale 专业版与基础版的区别是什么？",
                           vector_store=vector_store)


# In[20]:


display_answer(query="为什么我的项目没有获得创作者收益",
                           vector_store=vector_store)


# In[ ]:




