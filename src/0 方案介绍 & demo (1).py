#!/usr/bin/env python
# coding: utf-8

# # 基于本地知识的 ChatGLM 应用实现  
# ## 相关链接  
# 原项目Github：https://github.com/imClumsyPanda/langchain-ChatGLM  
# 
# ChatGLM-6B 在 ModelWhale 平台的部署与微调教程：https://www.heywhale.com/mw/project/6436d82948f7da1fee2be59e  
# 
# ## ModelWhale 运行配置  
# 计算资源：V100 Tensor Core GPU  
# 镜像：Python3.9 Cuda11.6 Torch1.12.1 官方镜像  
# 
# ## 介绍  
# 
# 🤖️ 一种利用 [ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B) + [langchain](https://github.com/hwchase17/langchain) 实现的基于本地知识的 ChatGLM 应用。  
# 
# 💡 受 [GanymedeNil](https://github.com/GanymedeNil) 的项目 [document.ai](https://github.com/GanymedeNil/document.ai) 和 [AlexZhangji](https://github.com/AlexZhangji) 创建的 [ChatGLM-6B Pull Request](https://github.com/THUDM/ChatGLM-6B/pull/216) 启发，建立了全部基于开源模型实现的本地知识问答应用。  
# 
# ✅ 本项目中 Embedding 选用的是 [GanymedeNil/text2vec-large-chinese](https://huggingface.co/GanymedeNil/text2vec-large-chinese/tree/main)，LLM 选用的是 [ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B)。依托上述模型，本项目可实现全部使用**开源**模型**离线私有部署**。  
# 
# ⛓️ 本项目实现原理如下图所示，过程包括加载文件 -> 读取文本 -> 文本分割 -> 文本向量化 -> 问句向量化 -> 在文本向量中匹配出与问句向量最相似的`top k`个 -> 匹配出的文本作为上下文和问题一起添加到`prompt`中 -> 提交给`LLM`生成回答。  
# 
# ![实现原理图](https://raw.githubusercontent.com/imClumsyPanda/langchain-ChatGLM/master/img/langchain%2Bchatglm.png)  
# 
# 🚩 本项目未涉及微调、训练过程，但可利用微调或训练对本项目效果进行优化。  
# 
# ## 本项目使用方式  
# 核心部分代码为  
# ```python  
# # 执行初始化  
# init_cfg(LLM_MODEL, EMBEDDING_MODEL, LLM_HISTORY_LEN)  
# # 使用 ChatGLM 的 readme 进行测试  
# vector_store = init_knowledge_vector_store("/home/mw/project/test_chatglm_readme.md")  
# ```
# 
# 其中vector_store的初始化可以传递 txt、docx、md 格式文件，或者包含md文件的目录。  
# 
# 更多知识库加载方式可以参考[langchain文档](https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/unstructured_file.html)，  
# 通过修改 init_knowledge_vector_store 方法进行兼容。  
# 
# **官方注**：ModelWhale GPU机型需要从云厂商拉取算力资源，耗时5~10min，且会预扣半小时资源价格的鲸币。如果资源未启动成功，预扣费用会在关闭编程页面后五分钟内退回，无需紧张，如遇问题欢迎[提报工单](https://www.heywhale.com/home/user/workorder)，客服会及时处理。  
# 
# ## 更新日志  
# [2023/05/11]  
# 1. 修复unstructured版本更新导致的PDF读取问题  
# 
# [2023/05/06]  
# 1. 更新 requirements。解决 langchain 版本导致的依赖冲突  
# 2. 同步上游代码结构，简化模块调用  
# 3. response 改为流式输出  
# 4. 真实案例知识库改为PDF格式  
# 
# [2023/04/28]  
# 1. 增加一个《动手学深度学习》书籍对话bot的真实案例  
# 2. 增加 ChineseTextSplitter 来避免召回内容过长导致的显存溢出问题  



# # 使用 Markdown 格式打印模型输出
# from IPython.display import display, Markdown, clear_output

def display_answer(agent, query, vs_path, history=[]):
    for resp, history in local_doc_qa.get_knowledge_based_answer(query=query,
                                                                 vs_path=vs_path,
                                                                 chat_history=history,
                                                                 streaming=True):
        clear_output(wait=True)
        display(Markdown(resp["result"]))
    return resp, history


# In[5]:


import torch.backends

from pkg.configs import model_config

# 全局参数，修改后请重新初始化
model_config.embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec-base": "shibing624/text2vec-base-chinese",
    "text2vec": "/home/mw/input/text2vec2538",
}
model_config.llm_model_dict = {
    "chatyuan": "ClueAI/ChatYuan-large-v2",
    "chatglm-6b-int4-qe": "THUDM/chatglm-6b-int4-qe",
    "chatglm-6b-int4": "THUDM/chatglm-6b-int4",
    "chatglm-6b-int8": "THUDM/chatglm-6b-int8",
    "chatglm-6b": "/home/mw/input/ChatGLM6B6449",
}
model_config.VS_ROOT_PATH = "/home/mw/temp"

# from chains.local_doc_qa import LocalDocQA

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




# 使用 ChatGLM 的 readme 进行测试
vs_path, _ = local_doc_qa.init_knowledge_vector_store("/home/mw/project/test_chatglm_readme.md")
vs_path


# 测试未进行本地知识库接入时的结果
# from IPython.display import display, Markdown, clear_output
for resp, history in local_doc_qa.llm._call("chatglm-6b 的局限性具体体现在哪里，如何实现改进"):
    clear_output(wait=True)
    display(Markdown(resp))



# 接入知识库后同一问题的返回结果
history = []
display_answer(local_doc_qa, query="chatglm-6b 的局限性具体体现在哪里，如何实现改进", vs_path=vs_path, history=history)

