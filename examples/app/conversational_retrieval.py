from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from lanarky import LangchainRouter

load_dotenv()

app = FastAPI(title="ConversationalRetrievalChainDemo")

templates = Jinja2Templates(directory="templates")


def create_chain():
    db = FAISS.load_local(
        folder_path="vector_stores/",
        index_name="langchain-python",
        embeddings=OpenAIEmbeddings(),
    )

    question_generator = LLMChain(
        llm=ChatOpenAI(
            temperature=0,
            streaming=True,
        ),
        prompt=CONDENSE_QUESTION_PROMPT,
    )
    doc_chain = load_qa_chain(
        llm=ChatOpenAI(
            temperature=0,
            streaming=True,
        ),
        chain_type="stuff",
    )

    return ConversationalRetrievalChain(
        combine_docs_chain=doc_chain,
        question_generator=question_generator,
        retriever=db.as_retriever(),
        return_source_documents=True,
        verbose=True,
    )


chain = create_chain()


langchain_router = LangchainRouter(
    langchain_url="/chat", langchain_object=chain, streaming_mode=1
)
langchain_router.add_langchain_api_route(
    "/chat_json", langchain_object=chain, streaming_mode=2
)

app.include_router(langchain_router)
