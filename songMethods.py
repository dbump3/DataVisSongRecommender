import numpy as np
import pandas as pd
import scipy.spatial

# read data
raw_data = pd.read_csv('data/tracks.csv')
data = np.array(raw_data[['id', 'name', 'artists', 'acousticness', 'danceability', 'energy', 'duration_ms', 'instrumentalness', 'valence', 'popularity', 'tempo', 'liveness', 'loudness', 'speechiness']])
song_names_lower = np.char.lower(np.array(data[:,1], dtype=str))
visited = set()


# Given a song ID, get the index of the song in data
def getIndexFromId(songId):
    return np.argwhere(data[:,0] == songId)[0][0]

# Given a song name, get the index of the song in data
def getIndexFromName(songName):
    return np.argwhere(data[:,1] == songName)[0][0]

# Given a song name, get the id of the song in data
def getIdFromName(songName):
    return data[getIndexFromName(songName)][0]

# Given a song ID, get the k most similar songs
def getKSimilarSongs(songName, k):
    songId, artists = data[getIndexFromName(songName)][0], data[getIndexFromName(songName)][2].strip('][\'').split(', ')
    root = [[songId, songName, artists, 0.0, None]]
    visited.clear()
    visited.add(songId)
    newData = data[0.0 < data[:,3]]
    # print(newData)
    return root + getKSimilarSongsHelper(songId, k, 0, newData)
    
def getKSimilarSongsHelper(songId, k, similarity, newData):
    # create new array with input song
    inputSong = np.expand_dims(newData[getIndexFromId(songId)], axis=0)

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
print(getKSimilarSongs("Easy Living (with Teddy Wilson & His Orchestra)", 4))