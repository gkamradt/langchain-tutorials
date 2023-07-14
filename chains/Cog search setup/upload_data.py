import os
import json 
import requests
import openai
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings

from dotenv import load_dotenv  
import os  
import openai
import os  
  

# Configure OpenAI API

AZURE_OPENAI_API_VERSION = "2023-03-15-preview"
AZURE_OPENAI_ENDPOINT ="https://cog-42as6n6i4ldsi.openai.azure.com/"
AZURE_OPENAI_API_KEY ="653103af9cd04492a2232b70327b7ce0"

# Set the ENV variables that Langchain needs to connect to Azure OpenAI
os.environ["OPENAI_API_BASE"] = os.environ["AZURE_OPENAI_ENDPOINT"] = AZURE_OPENAI_ENDPOINT
os.environ["OPENAI_API_KEY"] = os.environ["AZURE_OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY
os.environ["OPENAI_API_VERSION"] = os.environ["AZURE_OPENAI_API_VERSION"] = AZURE_OPENAI_API_VERSION
os.environ["OPENAI_API_TYPE"] = "azure"

COGNITIVE_SEARCH_INDEX = "azureblob-index"
COGNITIVE_SEARCH_HOSTNAME = "https://gptkb-42as6n6i4ldsi.search.windows.net"
COGNITIVE_SEARCH_API_KEY = "kSovyGNsoVRCGtovPviVe9Kibz7351x2Wb7RCHEjBRAzSeDWVLvj"
COGNITIVE_SEARCH_API_VERSION = "2023-07-01-preview"

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", chunk_size=1)
#load document from Azure blob storage and store in dataframe
import pandas as pd
import io
from azure.storage.blob import BlobServiceClient

# Define the connection string and container name
conn_str = "DefaultEndpointsProtocol=https;AccountName=entchatgptstr;AccountKey=gZss7VuVlbiwShlfML34GaeAw3QYEyicbZLF9D47zkGa/GCgx6jNGcNGBz0qqRa4Ci3MPqXrWI2O+AStm9gdMg==;EndpointSuffix=core.windows.net"
container_name = "pubmeddata"

# Create a BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(conn_str)

# Get a reference to the blob container
container_client = blob_service_client.get_container_client(container_name)

# Get a reference to the blob
blob_client = container_client.get_blob_client("df_test_embeddings10k.csv")

# Download the blob as a string
blob_string = blob_client.download_blob().content_as_text(encoding="utf-8")

# Load the string into a Pandas dataframe
df_test = pd.read_csv(io.StringIO(blob_string), encoding="utf-8")

# Print the dataframe
df_test.head()







data_json = json.load(open("sample_data.json"))

headers = {
    "Content-Type": "application/json",
    "api-key": COGNITIVE_SEARCH_API_KEY
}

upload_data = {
    "value": [
        {
            "@search.action": "upload",
            **data_json,
            "issue_statement_vector": embeddings.embed_query(data_json['issue_statement']),
            "comments_vector": embeddings.embed_query(data_json['comments']),
            "closure_comments_vector": embeddings.embed_query(data_json['closure_comments'])
        }
    ]
}

print(upload_data)

url = f"{COGNITIVE_SEARCH_HOSTNAME}/indexes/{COGNITIVE_SEARCH_INDEX}/docs/index?api-version={COGNITIVE_SEARCH_API_VERSION}"
response = requests.post(url, headers=headers, json=upload_data)
print(f"Uploaded data - Status {response.status_code}, message: {response.text}")