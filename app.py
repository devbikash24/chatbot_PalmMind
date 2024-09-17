from flask import Flask, render_template, request, jsonify
from src.chatagent import ChatBot
# from forms_agent import FormsAgent

app = Flask(__name__)

chat_agent = ChatBot()
# forms_agent = FormsAgent()

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/get', methods=['POST'])
def chat():
    user_message = request.form.get('msg')
    if user_message:
        response = chat_agent.handle_query(user_message)
        return response['response']
    return "Invalid Input", 400

@app.route('/form', methods=['POST'])
def handle_form():
    form_data = request.json
    response = forms_agent.process_form(form_data)
    return jsonify(response)

if __name__ == '__main__':
    
    app.run(debug=True)
