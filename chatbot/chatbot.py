from langchain.chat_models import init_chat_model
from langchain import hub
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import CSVLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langgraph.graph import START, StateGraph
from langchain_core.vectorstores import InMemoryVectorStore
import dotenv
from typing_extensions import List, TypedDict
import glob
import os
dotenv.load_dotenv()

def build_graph():
    dir_path = "../data/chatbot"
    csv_files = glob.glob(os.path.join(dir_path, "*.csv"))


    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)


    emb = OpenAIEmbeddings(model="text-embedding-3-large")

    store = InMemoryVectorStore(emb)

    for csv_file in csv_files:
        loader = CSVLoader(csv_file)
        docs = loader.load()
        splits = splitter.split_documents(docs)
        store.add_documents(splits)

    prompt = hub.pull("rlm/rag-prompt")

    llm = init_chat_model('gpt-3.5-turbo',model_provider='openai')

    class State(TypedDict):
        question: str
        context: List[Document]
        answer: str


    def retrieve(state: State):
        retrieved_docs = store.similarity_search(state["question"])
        return {"context": retrieved_docs}


    def generate(state: State):
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = prompt.invoke({"question": state["question"], "context": docs_content})
        response = llm.invoke(messages)
        return {"answer": response.content}


    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()
    return graph