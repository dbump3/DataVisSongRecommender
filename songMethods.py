import numpy as np
import pandas as pd
import scipy.spatial
from sklearn.preprocessing import normalize

# read data
raw_data = pd.read_csv('data/tracks.csv')
data = np.array(raw_data[['id', 'name', 'artists', 'popularity', 'duration_ms', 'danceability', 'instrumentalness', 'energy', 'valence', 'acousticness', 'tempo', 'liveness', 'loudness', 'speechiness']])

def normalize_data(data_in):
    for i in range(3, np.shape(data_in)[1]):
        data_min = np.min(data_in[:,i])
        data_max = np.max(data_in[:,i])
        first_part = data_in[:,:i]
        second_part = np.array([( data_in[:,i] + data_min ) / (np.max(data_in[:,i]) + data_min)]).T
        data_a = np.concatenate((first_part, second_part), axis=1)
        data_in = np.concatenate((data_a, data_in[:,i+1:]), axis=1)
    return data_in

data = normalize_data(data)
data = np.concatenate((data[:,:3], data[:,3:]), axis=1)
song_names_lower = np.char.lower(np.array(data[:,1], dtype=str))
visited = set()



# Given a song ID, get the index of the song in data
def getIndexFromId(newData, songId):
    print(newData[:,0])
    print(np.argwhere(newData[:,0] == songId))
    return np.argwhere(newData[:,0] == songId)[0][0]

# Given a song name, get the index of the song in data
def getIndexFromName(newData, songName):
    return np.argwhere(newData[:,1] == songName)[0][0]

# Given a song name, get the id of the song in data
def getIdFromName(songName):
    return data[getIndexFromName(data, songName)][0]

# Given a song ID, get the k most similar songs
def getKSimilarSongs(songName, k, filters):
    songIndex = getIndexFromName(data, songName)
    songId, artists = data[songIndex][0], data[songIndex][2].strip('][\'').split(', ')
    root = [[songId, songName, artists, 0.0, None]]
    visited.clear()
    visited.add(songId)
    newData = data
    for i in range(len(filters)):
        low, high = getRange(filters[i])
        newData = newData[low <= newData[:,i+3]]
        newData = newData[newData[:,i+3] <= high]
    # print(newData)
    return root + getKSimilarSongsHelper(songId, k, 0, newData)
    
def getRange(filter_val):
    if filter_val == "Any":
        return [0.0,1.0]
    elif filter_val == "Low" or filter_val == "Short":
        return [0.0,0.33]
    elif filter_val == "Medium":
        return [0.33,0.67]
    elif filter_val == "High" or filter_val == "Long":
        return [0.67,1.0]

def getKSimilarSongsHelper(songId, k, similarity, newData):
    # create new array with input song
    inputSong = np.expand_dims(data[getIndexFromId(data, songId)], axis=0)

    # get distance between input song and all other songs
    # note that the first column (id) is cut off since it is a string
    diff = scipy.spatial.distance.cdist(inputSong[:,3:], newData[:,3:], metric='euclidean')[0]
    
    # get k most similar indexes of songs
    kMostSimlarIndexes = np.argpartition(diff, k)[1:k+1]

    # return array containing k pairs of [songId, songName, artists, similarityRating, parentId]
    songs = (np.column_stack((newData[kMostSimlarIndexes][:,0],
                              newData[kMostSimlarIndexes][:,1],
                              newData[kMostSimlarIndexes][:,2],
                              diff[kMostSimlarIndexes],
                              [songId]*len(kMostSimlarIndexes)))).tolist()

    newSongs = []
    for song in songs:
        if song[3] != 0.0 and song[0] not in visited: # if similarity is 0, it's the same song so filter it out
            visited.add(song[0])
            song[3] += similarity # add parents similarity to root
            song[2] = song[2].strip('][\'').split(', ') # parse string representation of list of artists
            newSongs.append(song)

            # recursively add more songs with half as many songs at each step
            newK = k // 2
            if newK > 1:
                newSongs += getKSimilarSongsHelper(song[0], newK, song[3], newData) # add children

    return newSongs 

def finishSongName(partialName):
    partialName = partialName.lower()
    length = len(partialName)
    sliced_data = slicer_vectorized(song_names_lower, 0, length)
    indices = np.argwhere(sliced_data == partialName)
    song_names = data[indices][:,0][:,1][:8]
    return song_names.tolist()

def slicer_vectorized(a,start,end):
    b = a.view((str,1)).reshape(len(a),-1)[:,start:end]
    return np.array(b).view((str,end-start)).flatten()


# print(finishSongName("car"))
# sample input:
# print(getKSimilarSongs("Easy Living (with Teddy Wilson & His Orchestra)", 4))