from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

emb = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key="AIzaSyBcG6Dyxpjied6seYP4cjOf_dJ1COTQLLw"
)

print("Key loaded OK")
vec = emb.embed_query("hello world")
print("Embedding length:", len(vec))
