# SOURCE: https://towardsdatascience.com/talking-to-python-from-javascript-flask-and-the-fetch-api-e0ef3573c451

########  imports  ##########
from flask import Flask, jsonify, request, render_template
from songMethods import getIdFromName, getKSimilarSongs, finishSongName
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

@app.route('/getdata/<songName>', methods=['GET', 'POST'])
def data_get(songName):
    if request.method == 'GET': # GET request
        return jsonify(getKSimilarSongs(songName, 7)) # serialize and use JSON headers
    if request.method == 'POST': # POST request
        print(request.get_json()) # parse as JSON
        return 'Sucesss', 200

@app.route('/getsongid/<songName>', methods=['GET', 'POST'])
def song_id_get(songName):
    if request.method == 'GET': # GET request
        return jsonify(getIdFromName(songName)) # serialize and use JSON headers
    if request.method == 'POST': # POST request
        print(request.get_json()) # parse as JSON
        return 'Sucesss', 200

@app.route('/getauto/<partialName>', methods=['GET', 'POST'])
def get_songs(partialName):
    if request.method == 'GET':
        return jsonify(finishSongName(partialName))
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'Sucesss', 200
#########  run app  #########
app.run(debug=True)
