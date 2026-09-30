# Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/
# OpenAI Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/openai/

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()
import os
model_access = os.getenv("model")
print("Able to acess the model")
# Create a ChatOpenAI model
model = ChatOpenAI(model=model_access)

# Invoke the model with a message
result = model.invoke("What is 81 divided by 9?")
# print("Full result:", result)
# # print("Content only:",result.content)
# print(result.response_metadata.get("model_name"))
print(result.model_dump())