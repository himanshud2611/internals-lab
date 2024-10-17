import requests
from bs4 import BeautifulSoup
from langchain.schema import Document

class WebBaseLoader:
    def __init__(self, url:str):
        self.url = url

    def fetch_html(self):
        '''fetching the raw html content from the given url'''
        response = requests.get(self.url)
        response.raise_for_status()
        return response.text
    
    def parse_html(self, html_content:str):
        '''parsing html content using beautifulsoup'''
        soup = BeautifulSoup(html_content, "html.parser")
        '''removing script and style components'''
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        return soup.get_text()
    
    def clean_text(self, text:str):
        '''cleaning and normalizing the text'''
        lines = (line.strip() for line in text.splitlines())
        #chunks = (phrase.strip() for line in lines for phrase in line.split(" "))

        cleaned_text = '\n'.join(line for line in lines if line)
        return cleaned_text

    

    def load(self):
        '''loading the web page content and return as document'''
        html_content = self.fetch_html()
        parsed_text = self.parse_html(html_content)
        cleaned_text = self.clean_text(parsed_text)

        # returning a langchain document with the URL as metadata

        return Document(page_content=cleaned_text, metadata={"source": self.url})
    

# testing the code above
loader = WebBaseLoader("https://www.geeksforgeeks.org/what-is-an-operating-system/")
document = loader.load()
print(document.page_content)
