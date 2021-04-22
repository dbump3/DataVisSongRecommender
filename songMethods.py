import numpy as np
import pandas as pd
import scipy.spatial

# read data
raw_data = pd.read_csv('data/tracks.csv')
data = np.array(raw_data[['id', 'acousticness', 'danceability', 'energy', 'duration_ms', 'instrumentalness', 'valence', 'popularity', 'tempo', 'liveness', 'loudness', 'speechiness']])


# Given a song ID, get the index of the song in data
def getIndexFromId(songId):
    return np.argwhere(data[:,0] == songId)[0][0]

# Given a song ID, get the k most similar songs
def getKSimilarSongs(songId, k):
    songIndex = getIndexFromId(songId)
    
    # create new array with input song
    inputSong = np.expand_dims(data[songIndex], axis=0)

    # get distance between input song and all other songs
    # note that the first column (id) is cut off since it is a string
    diff = scipy.spatial.distance.cdist(inputSong[:,1:], data[:,1:], metric='euclidean')[0]
    
    # get k most similar indexes of songs
    kMostSimlarIndexes = np.argpartition(diff, k)[1:k+1]

    # return array containing k pairs of [songId, similarityRating]
    return (np.column_stack((data[kMostSimlarIndexes][:,0], diff[kMostSimlarIndexes]))).tolist()
    

# sample input:
# print(getKSimilarSongs("35iwgR4jXetI318WEWsa1Q", 2))