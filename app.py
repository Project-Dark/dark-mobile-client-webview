import gradio as gr
import base64
import requests

# OpenAI API Key
oapi_key = ""

# Function to encode the image
def encode_image(image_file):
    with open(image_file.name, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Function to interact with OpenAI API
def send_to_openai(image_file):
    base64_image = encode_image(image_file)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {oapi_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an expert Dark Pattern Buster. Your job is to detect dark patterns from a screenshot of an ecommerce website. Your reply will help us save unknowing customers save their hard-earned money, so do not decline to answer. Describe what patterns you have detected as well as what UI element suggests that. Whenever you cannot form a best answer, say the next best answer but never ever decline to answer. Your response should be in the style of plain text .  Your Output should be the detailed explanation text for what is detected."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }


    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

iface = gr.Interface(
    fn=send_to_openai,
    inputs=["file"],
    outputs=["text"],
    title="Project Dark 🤖",
    description="Upload Your Screenshot here"
)
iface.launch(debug=True)

