from flask import Flask, request, render_template, jsonify
from utils.payment_utils import create_invoice, verify_payment
from utils.user_utils import get_user_data, process_command, add_credit
from utils.approval_utils import submit_manual_payment, approve_manual_payment
import os
from utils.telegram_auth import check_auth, telegram_user

@app.route('/auth')
def telegram_auth():
    if not check_auth(request.args):
        return "❌ Authentication failed", 403
    user_id = request.args.get('id')
    return redirect(f'/dashboard/{user_id}')

app = Flask(__name__)

# === WebApp Home ===
@app.route('/')
def index():
    return render_template('index.html')

# === Dashboard ===
@app.route('/dashboard/<user_id>')
def dashboard(user_id):
    user = get_user_data(user_id)
    return render_template('dashboard.html', user=user)

# === Create ToyyibPay Invoice ===
@app.route('/create-invoice', methods=['POST'])
def create_invoice_route():
    data = request.get_json()
    url = create_invoice(data['user_id'], data['package'], data['amount'])
    return jsonify({'url': url})

# === Submit Command ===
@app.route('/submit-command', methods=['POST'])
def command_route():
    data = request.get_json()
    reply = process_command(data['user_id'], data['command'])
    return jsonify({'reply': reply})

# === Manual QR Payment Submission ===
@app.route('/upload-receipt', methods=['POST'])
def receipt():
    data = request.get_json()
    submit_manual_payment(data['user_id'], data['amount'], data['package'])
    return jsonify({'status': 'ok'})

# === Admin Manual Approval with Password ===
@app.route('/admin/approve/<user_id>', methods=['GET'])
def admin_approve(user_id):
    password = request.args.get('password')
    correct_pw = os.getenv('ADMIN_PASSWORD', 'letmein')
    if password != correct_pw:
        return "Unauthorized. Pass ?password=letmein in URL.", 403
    result = approve_manual_payment(user_id)
    return f"<pre>{result}</pre>"

# === Flask Run ===
if __name__ == '__main__':
    app.run(debug=True)
