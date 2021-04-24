import numpy as np
import pandas as pd
import scipy.spatial

# read data
raw_data = pd.read_csv('data/tracks.csv')
data = np.array(raw_data[['id', 'name', 'acousticness', 'danceability', 'energy', 'duration_ms', 'instrumentalness', 'valence', 'popularity', 'tempo', 'liveness', 'loudness', 'speechiness']])


# Given a song ID, get the index of the song in data
def getIndexFromId(songId):
    return np.argwhere(data[:,0] == songId)[0][0]

# Given a song name, get the index of the song in data
def getIndexFromName(songName):
    return np.argwhere(data[:,1] == songName)[0][0]

# Given a song ID, get the k most similar songs
def getKSimilarSongs(songName, k):
    songId = data[getIndexFromName(songName)][0]
    root = [[songId, songName, 0.0, None]]
    return root + getKSimilarSongsHelper(songId, k, 0)
    
def getKSimilarSongsHelper(songId, k, similarity):
    # create new array with input song
    inputSong = np.expand_dims(data[getIndexFromId(songId)], axis=0)

    # get distance between input song and all other songs
    # note that the first column (id) is cut off since it is a string
    diff = scipy.spatial.distance.cdist(inputSong[:,2:], data[:,2:], metric='euclidean')[0]
    
    # get k most similar indexes of songs
    kMostSimlarIndexes = np.argpartition(diff, k)[1:k+1]

    # return array containing k pairs of [songId, songName, similarityRating, parentId]
    songs = (np.column_stack((data[kMostSimlarIndexes][:,0],
                              data[kMostSimlarIndexes][:,1],
                              diff[kMostSimlarIndexes],
                              [songId]*len(kMostSimlarIndexes)))).tolist()

    newSongs = []
    for song in songs:
        if song[2] != 0.0: # if similarity is 0, it's the same song so filter it out
            print(song[2])
            song[2] += similarity # add parents similarity to root
            newSongs.append(song)

            # recursively add more songs with half as many songs at each step
            newK = k // 2
            if newK > 1:
                newSongs += getKSimilarSongsHelper(song[0], newK, song[2]) # add children

    return newSongs 

# sample input:
# print(getKSimilarSongs("Easy Living (with Teddy Wilson & His Orchestra)", 4))