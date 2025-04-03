from flask import Flask, render_template, request, jsonify
from utils.payment_utils import create_invoice, verify_payment
from utils.user_utils import get_user_data, process_command
from utils.approval_utils import submit_manual_payment
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard/<user_id>')
def dashboard(user_id):
    user_data = get_user_data(user_id)
    return render_template('dashboard.html', user=user_data)

@app.route('/submit-command', methods=['POST'])
def submit_command():
    data = request.json
    user_id = data.get('user_id')
    command = data.get('command')
    reply = process_command(user_id, command)
    return jsonify({"reply": reply})

@app.route('/create-invoice', methods=['POST'])
def invoice():
    data = request.json
    user_id = data['user_id']
    package = data['package']
    amount = data['amount']
    url = create_invoice(user_id, package, amount)
    return jsonify({"url": url})

@app.route('/verify-payment', methods=['GET'])
def verify():
    bill_code = request.args.get('billCode')
    user_id = request.args.get('user_id')
    if verify_payment(bill_code, user_id):
        return jsonify({"status": "success"})
    return jsonify({"status": "manual"})

@app.route('/upload-receipt', methods=['POST'])
def manual_upload():
    data = request.json
    user_id = data['user_id']
    amount = data['amount']
    package = data['package']
    submit_manual_payment(user_id, amount, package)
    return jsonify({"status": "pending"})

if __name__ == '__main__':
    app.run(debug=True)
