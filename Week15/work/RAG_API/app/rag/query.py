from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import time
import logging

from app.config import settings
from app.rag.store import store_manager
from app.privacy import mask_private_data


logger = logging.getLogger("fastapi_rag.query")

PROMPT = ChatPromptTemplate.from_template("""
You are an HR Support Assistant.

Answer employee questions using ONLY the provided company documents.
If the answer is not found in the documents, say:
"I’m not sure based on current HR policies."

Be clear, professional, and policy-aligned.

HR Context:
{context}

Employee Question:
{question}
""".strip())

def answer_query(user_query: str, index_path: str, k: int, *, sanitize: bool, sanitize_context: bool):
    vs = store_manager.load(index_path)
    retriever = vs.as_retriever(search_kwargs={"k": k})

    docs = retriever.invoke(user_query)
    context = "\n\n".join(d.page_content for d in docs)

    sanitized_query = mask_private_data(user_query) if sanitize else user_query
    sanitized_context = mask_private_data(context) if (sanitize and sanitize_context) else context

    # Log what goes into the model (privacy-safe if sanitize=True)
    logger.info(
        "pre-model | sanitize=%s | k=%s | sanitized_query=%r | context_chars=%d",
        sanitize, k, sanitized_query, len(sanitized_context)
    )

    llm_kwargs = {"model": settings.llm_model, "temperature": 0}
    if settings.openai_api_base:
        llm_kwargs["base_url"] = settings.openai_api_base
    if settings.openai_api_key:
        llm_kwargs["api_key"] = settings.openai_api_key

    llm = ChatOpenAI(**llm_kwargs)

    msg = llm.invoke(PROMPT.format_messages(context=sanitized_context, question=user_query))
    return msg.content, docs, sanitized_query