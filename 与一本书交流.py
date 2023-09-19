#!/usr/bin/env python
# coding: utf-8


# PDF位置：/home/mw/project/d2l-zh-pytorch-2.0.0.pdf
# 安装依赖
# !pip install -r requirements.txt -i https://mirror.sjtu.edu.cn/pypi/web/simple

# 安装nltk_data
# 已有的情况下需要给出目录
# !cp -r nltk_data /root/autodl-tmp/langchain-ChatGLM




# 使用 Markdown 格式打印模型输出
# from IPython.display import display, Markdown, clear_output

def display_answer(agent, query, vs_path, history=[]):
    for resp, history in local_doc_qa.get_knowledge_based_answer(query=query,
                                                                 vs_path=vs_path,
                                                                 chat_history=history,
                                                                 streaming=True):
        clear_output(wait=True)
        # display(Markdown(resp["result"]))
    return resp, history


import torch.backends

from configs import model_config



# 全局参数，修改后请重新初始化
model_config.embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec-base": "shibing624/text2vec-base-chinese",
    "text2vec": "/root/autodl-tmp/text2vec-large-chinese", # /home/mw/input/text2vec2538
}
model_config.llm_model_dict = {
    "chatyuan": "ClueAI/ChatYuan-large-v2",
    "chatglm-6b-int4-qe": "THUDM/chatglm-6b-int4-qe",
    "chatglm-6b-int4": "THUDM/chatglm-6b-int4",
    "chatglm-6b-int8": "THUDM/chatglm-6b-int8",
    "chatglm-6b": "/root/autodl-tmp/model/chatglm-6b", # /home/mw/input/ChatGLM6B6449
}

# /root/autodl-tmp/temp
model_config.VS_ROOT_PATH = "/root/autodl-tmp/temp" #/home/mw/temp 



from chains.local_doc_qa import LocalDocQA

EMBEDDING_MODEL = "text2vec" # embedding 模型，对应 embedding_model_dict
VECTOR_SEARCH_TOP_K = 6
LLM_MODEL = "chatglm-6b"     # LLM 模型名，对应 llm_model_dict
LLM_HISTORY_LEN = 3
DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

local_doc_qa = LocalDocQA()

local_doc_qa.init_cfg(llm_model=LLM_MODEL,
                          embedding_model=EMBEDDING_MODEL,
                          llm_history_len=LLM_HISTORY_LEN,
                          top_k=VECTOR_SEARCH_TOP_K)


# # 构建本地文件库

# In[5]:


# !pip install tabulate


# vs_path, _ = local_doc_qa.init_knowledge_vector_store("/root/autodl-tmp/test") # /home/mw/project/d2l-zh-pytorch-2.0.0.pdf

# 构建全量模型
vs_path, _ = local_doc_qa.init_knowledge_vector_store("/root/autodl-tmp/track2-问答式科研知识库") # /home/mw/project/d2l-zh-pytorch-2.0.0.pdf



# In[ ]:





# In[ ]:





# # 读取本地知识库并对话

# In[15]:


# 知识库过大会导致分配空间失败


# In[14]:


vs_path  = '/root/autodl-tmp/papers_FAISS' # 完成知识库


# In[12]:


import torch
torch.backends.cuda.max_split_size_mb = 512


# In[13]:


# 可以额外返回参照的知识库源信息
history = []
resp, history = display_answer(local_doc_qa, query="什么是 DenseNet 模型", vs_path=vs_path, history=history)
# print(resp)
# resp["source_documents"]


# In[ ]:





# In[7]:


history


# In[8]:


# 多轮对话
resp, history = display_answer(local_doc_qa, query="它与ResNet的关键区别是什么？", vs_path=vs_path, history=history)
print()


# In[9]:


resp["source_documents"]


# In[ ]:




