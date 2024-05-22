import os
from dotenv import load_dotenv
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.audio import OpenAIWhisperParser
from langchain_community.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain_together import Together
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain

load_dotenv()

url = "https://www.youtube.com/watch?v=-3toF-B2lEk"

save_dir = "docs/youtube"
loader = GenericLoader(
    YoutubeAudioLoader([url], save_dir),
    OpenAIWhisperParser()
)
docs = loader.load()

prompt = PromptTemplate(
    template="""Summarize the main points and their comprehensive explanations from below text, presenting them under appropriate headings. Use various Emoji to symbolize different sections, and format the content as a cohesive paragraph under each heading. Ensure the summary is clear, detailed, and informative, reflecting the executive summary style found in news articles. Avoid using phrases that directly reference 'the script provides' to maintain a direct and objective tone. \
    ```{text}```
    """,
    input_variables=["text"]
)

combine_prompt = PromptTemplate(
    template="""Summarize the main points and their comprehensive explanations from the provided text, organizing them under appropriate headings and using various Emoji to symbolize different sections. Format the content as a cohesive paragraph under each heading, ensuring clarity, detail, and informativeness akin to the executive summary style found in news articles. Maintain a direct and objective tone without directly referencing 'the script provides'. \
    ```{text}```
    """,
    input_variables=["text"]
)

together_llm = Together(
    model="meta-llama/Llama-3-70b-chat-hf",
    temperature=0,
    max_tokens=128,
    top_k=1,
    together_api_key=os.environ.get("TOGETHER_API_KEY")
)

summarize_chain = load_summarize_chain(
    together_llm,
    chain_type="map_reduce",
    map_prompt=prompt,
    combine_prompt=combine_prompt
)

result = summarize_chain.invoke(docs)
print(result["output_text"])

# Example output:
# **Summary** 📚
#
# **The React Compiler Solution** 🎉
# The React compiler is a game-changer for optimizing React applications, providing a solution to the long-standing memoization issues that have plagued developers.
#
# **The Memoization Conundrum** 🤔
# Memoization has been a contentious topic in React development, with many questions surrounding its use, including when to employ it, how to use it correctly, and the role of `useCallback` and `useMemo`. Some developers have even opted out of using memoization, deeming it too cumbersome

