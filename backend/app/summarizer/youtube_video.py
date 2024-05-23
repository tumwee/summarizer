import os
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.audio import OpenAIWhisperParser
from langchain_community.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain_together import Together
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain


def summarize(url):
    save_dir = "docs/youtube"
    loader = GenericLoader(
        YoutubeAudioLoader([url], save_dir),
        OpenAIWhisperParser()
    )
    docs = loader.load()
    remove_video_files(docs)

    prompt = PromptTemplate(
        template="""Summarize the main points and their comprehensive explanations from below text, presenting them under appropriate headings. Use various Emoji to symbolize different sections, and format the content as a cohesive paragraph under each heading. Ensure the summary is clear, detailed, and informative, reflecting the executive summary style found in news articles. Avoid using phrases that directly reference 'the script provides' to maintain a direct and objective tone. \
        ```{text}```
        """,
        input_variables=["text"]
    )

    together_llm = Together(
        model="meta-llama/Llama-3-70b-chat-hf",
        temperature=0,
        max_tokens=1024,
        top_k=1,
        together_api_key=os.environ.get("TOGETHER_API_KEY")
    )

    summarize_chain = load_summarize_chain(
        together_llm,
        chain_type="stuff",
        prompt=prompt,
    )

    result = summarize_chain.invoke(docs)

    return result["output_text"]


def remove_video_files(docs):
    for doc in docs:
        if os.path.exists(doc.metadata['source']):
            os.remove(doc.metadata['source'])
