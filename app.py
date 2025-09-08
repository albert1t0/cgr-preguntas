from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from werkzeug.utils import secure_filename
import PyPDF2
import pptx
import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Configure the Gemini API key
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("La variable de entorno GOOGLE_API_KEY no está configurada o el archivo .env no se encontró.")
    genai.configure(api_key=api_key)
except (KeyError, ValueError) as e:
    # This will stop the app from starting if the key is not found
    raise SystemExit(e)


def extract_text(filepath):
    ext = filepath.rsplit('.', 1)[1].lower()
    text = ""
    if ext == 'pdf':
        try:
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text()
        except PyPDF2.errors.PdfReadError:
            return "Error: No se pudo leer el archivo PDF. Puede que esté corrupto o encriptado."
    elif ext == 'pptx':
        try:
            prs = pptx.Presentation(filepath)
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + "\n"
        except Exception as e:
            return f"Error: No se pudo leer el archivo PPTX. {e}"
    return text

def generate_quiz(text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = '''
    Basándote en el siguiente texto, genera un cuestionario de 2 preguntas de opción múltiple.
    El formato de salida debe ser un objeto JSON válido y nada más. No incluyas '```json' o '```' en la salida.
    La estructura debe ser la siguiente:
    {
      "preguntas": [
        {
          "pregunta": "¿Tu pregunta aquí?",
          "opciones": ["Opción A", "Opción B", "Opción C", "Opción D"],
          "respuesta_correcta_index": 2,
          "justificacion": "La justificación de por qué la respuesta es correcta."
        },
        {
          "pregunta": "¿Tu segunda pregunta aquí?",
          "opciones": ["Opción 1", "Opción 2", "Opción 3", "Opción 4"],
          "respuesta_correcta_index": 0,
          "justificacion": "La justificación de la segunda respuesta."
        }
      ]
    }

    Texto de contexto:
    ''' + text

    try:
        response = model.generate_content(prompt)
        # Clean the response to get only the JSON part
        json_response_cleaned = response.text.strip().replace("```json", "").replace("```", "")
        quiz = json.loads(json_response_cleaned)
        return quiz
    except Exception as e:
        # It's better to return the error and handle it in the route
        return {"error": f"Error al generar o parsear el cuestionario desde Gemini: {e}", "raw_response": response.text if 'response' in locals() else "No response"}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        extracted_text = extract_text(filepath)
        if extracted_text.startswith("Error:"):
            return f"<h1>Error en la extracción de texto</h1><p>{extracted_text}</p>", 400

        quiz_data = generate_quiz(extracted_text)

        if "error" in quiz_data:
             return f"<h1>Error al generar el Quiz</h1><pre>{json.dumps(quiz_data, indent=2)}</pre>", 500

        # Render the quiz template with the data
        rendered_html = render_template('quiz.html', quiz_data=quiz_data)

        # Save the rendered HTML to a file
        output_filename = f"test_{os.path.splitext(filename)[0]}.html"
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(rendered_html)

        # Send the generated file to the user for download
        return send_file(output_filepath, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5001)
