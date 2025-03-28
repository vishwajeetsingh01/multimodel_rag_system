from src.pdf_handler.pdf_handler import PdfHandler
from src.llama_handler.llama_handler import LlamaHandler
from flask import Flask, request, jsonify, render_template
import logging.config
from src.config import config

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(funName)s:%(lineno)d - %(message)s',handlers=[logging.FileHandler("logging.log")])
app.logger.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# Instance of LlamaHandler
llama_handler = LlamaHandler(text_embed_model=config.TEXT_EMBEDDING_MODEL, image_embed_model=config.IMAGE_EMBEDDING_MODEL, llm=None, nm_llm='llava')
#llama_handler = LlamaHandler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/persist', methods=['POST'])
def pipeline_v1_persist():
    try:
        pdf_handler = PdfHandler()
        pdf_handler.process_pdfs()
        llama_handler.pipeline_v1_persist()
        return jsonify({'message': 'pipeline v1 persisted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/answer', methods=['POST'])    
def asnwer():
    try:
        question = request.json['question']
        response = llama_handler.multi_model_answer_engine(question)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#testing another pipeline    
@app.route('/persist', methods=['POST'])
def pipeline_v3_persist():
    try:
        pdf_handler = PdfHandler()
        pdf_handler.process_pdfs()
        llama_handler.pipeline_v3_persist()
        return jsonify({'message': 'pipeline v3 persisted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500    
    
@app.route('/answer_v3', methods=['POST'])    
def asnwer():
    try:
        question = request.json['question']
        response = llama_handler.multi_model_answer_engine(question)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500   

if __name__ == '__main__':
    app.run(debug=False)     