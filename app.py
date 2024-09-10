from flask import Flask, request, jsonify, render_template
import openai
import re
import os
from pypdf import PdfReader

app = Flask(__name__)

# Configura tu clave de API de OpenAI
openai.api_key = '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'

def extract_text_from_pdf(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_all_pdfs_in_folder(folder_path):
    all_text = ""
    for filename in os.listdir(folder_path):
        print(filename)
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            title = os.path.splitext(filename)[0]
            text = extract_text_from_pdf(pdf_path)
            all_text += f"\n\n{title}\n\n{text}\n"
    return all_text

def ask_question(prompt, question):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant. The first prompt will be a long text,'
                                            'and any messages that you get be regarding that. Please answer any '
                                            'questions and requests having in mind the first prompt '},
            {'role': 'user', 'content': prompt},
            {'role': 'user', 'content': question}
        ]
    )
    return response.choices[0].message['content']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    print("Hola")
    data = request.get_json()
    question = data.get('question')
    course = data.get('course')
    question = "Hola, responde usando solo el texto enviado" + question

    folder_paths = {
        'religion': 'files/religion',
        'biologia': 'files/biologia',
        'fisica': 'files/fisica'
    }

    if course in folder_paths:
        folder_path = folder_paths[course]
        file_content = extract_text_from_all_pdfs_in_folder(folder_path)
        response = ask_question(file_content, question)
        print("llego ahsta aqui")
        formatted_response = re.sub(r'(\. )', '.\n', response)
        print(response)
        return jsonify({'response': formatted_response})
    else:
        return jsonify({'response': 'Invalid course selected'})


if __name__ == '__main__':
    app.run(debug=True)
