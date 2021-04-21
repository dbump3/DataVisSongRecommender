########  imports  ##########
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

#############################
# Additional code goes here #
#############################
@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def testfn():    # GET request
    if request.method == 'GET':
        message = {'greeting':'Hello from Python Flask!'}
        return jsonify(message)  # serialize and use JSON headers    # POST request
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'Sucesss', 200

#########  run app  #########
app.run(debug=True)