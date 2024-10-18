import openai
import gradio as gr
from transformers import pipeline
from flask import Flask, request, jsonify

app = Flask(__name__)

# OpenAI API Key (Make sure to replace with your actual API key)
openai.api_key = ''

# Hugging Face Summarization, Translation, and Sentiment Analysis pipelines
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
translator_en_to_fr = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
translator_en_to_de = pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-en-de")
translator_en_to_es = pipeline("translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es")
sentiment_analyzer = pipeline("sentiment-analysis")

# Function to generate OpenAI Chat Completion response
def chat_response(input_text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=input_text,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Function to generate summarization
def summarize_text(input_text):
    summary = summarizer(input_text, max_length=50, min_length=25, do_sample=False)
    return summary[0]['summary_text']

# Functions to translate text into multiple languages
def translate_text(input_text, language):
    if language == "French":
        translation = translator_en_to_fr(input_text)
    elif language == "German":
        translation = translator_en_to_de(input_text)
    elif language == "Spanish":
        translation = translator_en_to_es(input_text)
    return translation[0]['translation_text']

# Function to analyze sentiment
def analyze_sentiment(input_text):
    sentiment = sentiment_analyzer(input_text)
    return f"Sentiment: {sentiment[0]['label']}, Score: {sentiment[0]['score']:.2f}"

# Function to handle chatbot interaction
def chatbot(input_text, mode, language=None):
    if mode == "Chat Response":
        return chat_response(input_text)
    elif mode == "Summarization":
        return summarize_text(input_text)
    elif mode == "Translation":
        if language:
            return translate_text(input_text, language)
        else:
            return "Please select a language for translation."
    elif mode == "Sentiment Analysis":
        return analyze_sentiment(input_text)
    else:
        return "Invalid mode selected!"

# Creating Gradio interface
interface = gr.Interface(
    fn=chatbot,
    inputs=[
        gr.Textbox(lines=7, placeholder="Type your text here..."), 
        gr.Radio(["Chat Response", "Summarization", "Translation", "Sentiment Analysis"]),
        gr.Dropdown(["French", "German", "Spanish"], label="Select language (For Translation)")  # Removed 'optional=True'
    ],
    outputs="text",
    title="AI-Powered Chatbot with Enhanced Features",
    description="Ask questions, get summaries, translate text to multiple languages, or analyze sentiment.",
    theme="compact",
)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    input_text = data.get('input_text')
    mode = data.get('mode')
    language = data.get('language')

    if mode == 'Chat':
        response = f"Chatbot response to '{input_text}'"
    elif mode == 'Summarization':
        response = f"Summarized version of '{input_text}'"
    elif mode == 'Translation':
        response = translate_text(input_text, language)
    elif mode == 'Sentiment Analysis':
        response = analyze_sentiment(input_text)
    else:
        response = "Invalid mode selected."

    return jsonify({'response': response})

# Launching the Gradio app
if __name__ == "__main__":
    interface.launch()
