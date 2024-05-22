from dotenv import load_dotenv
from together import Together
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.audio import OpenAIWhisperParser
from langchain_community.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader

load_dotenv()

url = "https://www.youtube.com/watch?v=-3toF-B2lEk"
save_dir = "docs/youtube"
loader = GenericLoader(
    YoutubeAudioLoader([url], save_dir),
    OpenAIWhisperParser()
)
docs = loader.load()
print(docs[0].page_content[0:500])
