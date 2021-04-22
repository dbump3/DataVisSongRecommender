# SOURCE: https://towardsdatascience.com/talking-to-python-from-javascript-flask-and-the-fetch-api-e0ef3573c451

########  imports  ##########
from flask import Flask, jsonify, request, render_template
from songMethods import getKSimilarSongs
app = Flask(__name__)

#############################
# Additional code goes here #
#############################
# # read file
# with open('./data/track_names.json', 'r') as myfile:
#     data = myfile.read()

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/getdata/<song>', methods=['GET', 'POST'])
def data_get(song):    # GET request
    if request.method == 'GET':
        return jsonify(getKSimilarSongs(song, 2))  # serialize and use JSON headers    # POST request
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'Sucesss', 200

#########  run app  #########
app.run(debug=True)
