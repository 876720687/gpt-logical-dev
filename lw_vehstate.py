'''
Important references
langchain memory: https://www.bilibili.com/video/BV1sW4y1Q7br/?p=12&vd_source=95dc74fe4849b1d1ed162ed360aadca8
langchain vector db: https://python.langchain.com/docs/modules/chains/popular/vector_db_qa
prompt techniques: https://mp.weixin.qq.com/s/zmEGzm1cdXupNoqZ65h7yg
How LLM impacts engineers: https://mp.weixin.qq.com/s/_Kh8IzsfghT4fPWknesnzA

! yum install python3
! pip install langchain
! pip install openai
! pip install PyPDF2
! pip install tiktoken
! pip install faiss-cpu
'''
from langchain import FAISS
from langchain.chains import RetrievalQA
from langchain.chains import ConversationChain  # 本身带有记忆功能
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from string import Template
from prompt_engineer import def_queries, fds_q_templates, qa_q_templates
import os
import time
import ast

# idl_path = './idl_wiper.pdf'
plans = [{"chapter": "Front Wiper Function Enable Evaluation (FrntWiprTyp = mechanical wiper)"}]  # array of plans
gpt_model = "gpt-4"
# gpt_model = "gpt-3.5-turbo-16k-0613"
os.environ["OPENAI_API_KEY"] = "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"
######## debug flag ########
def_enable = True
fds_enable = True
idl_enable = False
qa_enable = True


def def_qa(def_queries, llm, memory_array):
    print("######## teach gpt definitions of new concepts ########")

    def_chain = ConversationChain(
        llm=llm,
        memory=memory_array[0],
        verbose=False)

    i = 1
    for def_q in def_queries:
        print("DEF_Q" + str(i) + ": " + def_q + "\n")
        time.sleep(16)
        ret = def_chain.run(def_q)
        print("DEF_A" + str(i) + ":\n" + ret + "\n\n\n")
        i = i + 1
        for j in range(1, len(memory_array)): # 只有预定义的信息需要做到所有记忆体全部更新
            memory_array[j].save_context({"input": def_q}, {"output": ret})


def fds_qa(chapter, llm, fds_q_templates, fds_retriever, memory):
    print("######## query fds for {chapter} ########".format(chapter=chapter))

    fds_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=fds_retriever,
        return_source_documents=False)

    fds_queries = []
    for fds_q_template in fds_q_templates:
        fds_queries.append(fds_q_template.substitute(chapter=plan["chapter"]))

    i = 1
    for fds_q in fds_queries:
        print("FDS_Q, {chapter}, {index}: {question}\n".format(chapter=chapter, index=i, question=fds_q))
        time.sleep(16)
        ret = fds_chain({"query": fds_q})
        memory.save_context({"input": fds_q}, {"output": ret["result"]})
        print("FDS_A, {chapter}, {index}:\n {answer}\n\n\n".format(chapter=chapter, index=i, answer=ret["result"]))
        i = i + 1
    signal_dic = ast.literal_eval(ret["result"])
    signals = signal_dic.keys()
    print("\nIdentified signals:\n " + str(signals) + "\n")
    return signals  # 最终返回的是信号？


# def idl_qa(chapter, llm, signals, idl_retriever, memory):
#     print("\n######## query idl for signal values of in {chapter} ########\n".format(chapter=chapter))
#
#     idl_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=idl_retriever,
#         return_source_documents=False)
#
#     q_template = '''
# The signal definition is written in a form.
# Look up {signal} in signal definition and make your best guess
# about its possible values. Use exact match for signal names.
# Explicitly highlight the mapping between enum values and
# integer values in the format of [integer value]: [enum value].
# In case you cannot find the signal, explicitly say sorry.
# '''
#
#     output = ''
#     defined_signals = []
#     not_defined_signals = []
#     for signal in signals:
#         signal = signal.strip()
#         print("#### Looking up signal: " + signal)
#         q = q_template.format(signal=signal)
#         time.sleep(16)
#         ret = idl_chain.run(q)
#         print("#### Lookup result for signal : " + signal + "\n" + ret + "\n\n")
#         if "sorry" not in ret:
#             defined_signals.append(signal)
#             output = output + "\n\n" + ret
#         else:
#             not_defined_signals.append(signal)
#
#     p = '''
# We call this query and its answer the "documented signal values".
# Its purpose is to identify all the defined signales' values: {defined_signals}.
# It also highlights the signals that are not defined: {not_defined_signals}.
# '''.format(defined_signals=str(defined_signals),
#            not_defined_signals=str(not_defined_signals))
#     memory.save_context({"input": p}, {"output": output})
#     print("IDL_Q signal values:\n {question}\n".format(question=p))
#     print("IDL_A signal values:\n" + output + "\n\n\n")


def gpt_qa(chapter, llm, qa_q_templates, memory):
    print("\n######## query chatgpt for of {chapter} ########\n".format(chapter=chapter))

    qa_chain = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True)

    qa_queries = []
    for qa_q_template in qa_q_templates:
        qa_queries.append(qa_q_template.substitute(chapter=plan["chapter"]))

    i = 1
    for qa_q in qa_queries:
        print("QA_Q, {chapter} {index}: {question}\n".format(chapter=chapter, index=i, question=qa_q))
        time.sleep(16)
        ret = qa_chain.predict(input=qa_q)
        print("QA_A, {chapter} {index}:\n {answer}\n\n\n".format(chapter=chapter, index=i, answer=ret))
        i = i + 1




# 1、 构建对应本地知识库
# 2、 构建逻辑对话
# 3、 喂本地知识进行问答
# 4、 进行提问

llm = ChatOpenAI(model_name=gpt_model, temperature=0.0)
fds_retriever = FAISS.load_local("local_docs", OpenAIEmbeddings()).as_retriever(search_type="similarity",
                                                                                search_kwargs={"k": 5})

#### def doc qa chains for each plan, do def_chain only once to save money ####
# 为每一个plan构建对应的记忆缓存,也就是一个章节存储一个
plan_index = -1
memory_array = []  # 信息存储-> at what condition this array is useful? 为什么不用ConversationBufferMemory？
for plan in plans:
    plan_index = plan_index + 1
    memory = ConversationBufferMemory(memory_key="history", return_messages=True)
    memory_array.append(memory)

# from buffer_wiper import buffer_input, buffer_output # self define
plan_index = -1
for plan in plans:
    plan_index = plan_index + 1
    memory = memory_array[plan_index]
    chapter = plan["chapter"]

    if def_enable and plan_index == 0:
        def_qa(def_queries, llm, memory_array)  # 询问产生输出, 并将对话内容保存回memory array

    signals = []
    if fds_enable:
        signals = fds_qa(chapter
                         , llm
                         , fds_q_templates  # 模板
                         , fds_retriever  # 检索器
                         , memory)

    # if idl_enable:
    #     idl_qa(chapter, llm, signals, idl_retriever, memory)
    # # 自建一个缓冲池即可
    # else:
    #     for k in range(len(buffer_input)):
    #         print("Q " + str(k) + ":\n" + buffer_input[k] + "\n")
    #         print("A " + str(k) + ":\n" + buffer_output[k] + "\n")
    #         memory.save_context({"input": buffer_input[k]}, {"output": buffer_output[k]})

    if qa_enable:
        gpt_qa(chapter, llm, qa_q_templates, memory)

print("process finished.")
