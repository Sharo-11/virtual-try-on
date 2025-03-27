from flask import Flask, request, jsonify, render_template
from PIL import Image
import requests
from io import BytesIO
import base64
import urllib3

# Disable warnings for unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/preds", methods=['POST'])
def submit():
    cloth = request.files['cloth']
    model = request.files['model']

    url = "https://4554-110-224-125-209.ngrok-free.app/"
    print(f"Using URL: {url}")  # Debugging statement
    print("Sending request...")

    try:
        # Disable SSL verification for this request
        response = requests.post(url=url, files={"cloth": cloth.stream, "model": model.stream}, verify=False)
        print(f"Response status code: {response.status_code}")  # Debugging statement
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")  # Handle exceptions
        return render_template('index.html', error="An error occurred while sending the request.")

    # Check if the request was successful
    if response.status_code == 200:
        op = Image.open(BytesIO(response.content))
        print(op)
        buffer = BytesIO()
        op.save(buffer, 'png')
        buffer.seek(0)

        data = buffer.read()
        data = base64.b64encode(data).decode()
        
        return render_template('index.html', op=data)
    else:
        return render_template('index.html', error="Failed to get a valid response from the server.")

if __name__ == '__main__':
    app.run(debug=True)
