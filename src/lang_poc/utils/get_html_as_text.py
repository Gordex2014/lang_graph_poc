import os
import requests
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from constants.temp import TEMP_DIR
from utils.hash import hash_md5

def get_html_as_text(url: str) -> str:
    """
    Fetch HTML content from a URL, cache it, and convert it to text.
    
    Args:
        url: The URL to fetch HTML from
        
    Returns:
        The extracted text content
        
    Raises:
        Exception: If fetching or processing fails
    """
    
    try:
        url_hash = hash_md5(url)
        
        # Create temp directory if it doesn't exist
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)
            
        url_directory = os.path.join(TEMP_DIR, f"{url_hash}.html")
        
        html = None
        
        # Check if cached version exists
        if os.path.exists(url_directory):
            with open(url_directory, "r", encoding="utf-8") as file:
                html = file.read()
        else:
            # Fetch and cache the HTML
            response = requests.get(url)
            if not response.ok:
                raise Exception(f"Failed to fetch {url}")
            
            html = response.text
            with open(url_directory, "w", encoding="utf-8") as file:
                file.write(html)
                
        # Process the HTML with UnstructuredLoader
        loader = UnstructuredHTMLLoader(url_directory)
        loaded_doc = loader.load() # Using sync version
        
        # Split the document
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        split_docs = text_splitter.split_documents(loaded_doc)
        combined_text = "\n\n".join([doc.page_content for doc in split_docs])
        
        return combined_text
    except Exception as e:
        print(f"Error: {e}")
        raise
        
