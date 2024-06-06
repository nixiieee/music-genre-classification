import librosa
import numpy as np
import pandas as pd
import pickle
from catboost import CatBoostClassifier
from sklearn.preprocessing import MinMaxScaler

model = CatBoostClassifier()
model.load_model('model.pickle')
scaler = pickle.load(open('scaler.pickle', 'rb'))
classes = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']

def extract_features(audio_file, sr):
    features = {}
    
    chroma = librosa.feature.chroma_stft(y=audio_file, sr=sr)
    features['chroma_stft_mean'] = [np.mean(chroma)]
    features['chroma_stft_var'] = [np.var(chroma)]

    rms = librosa.feature.rms(y=audio_file)
    features['rms_mean'] = [np.mean(rms)]
    features['rms_var'] = [np.var(rms)]

    spectral_centroid = librosa.feature.spectral_centroid(y=audio_file, sr=sr)
    features['spectral_centroid_mean'] = [np.mean(spectral_centroid)]
    features['spectral_centroid_var'] = [np.var(spectral_centroid)]
    
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio_file, sr=sr)
    features['spectral_bandwidth_mean'] = [np.mean(spectral_bandwidth)]
    features['spectral_bandwidth_var'] = [np.var(spectral_bandwidth)]
    
    rolloff = librosa.feature.spectral_rolloff(y=audio_file, sr=sr)
    features['rolloff_mean'] = [np.mean(rolloff)]
    features['rolloff_var'] = [np.var(rolloff)]
    
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y=audio_file)
    features['zero_crossing_rate_mean'] = [np.mean(zero_crossing_rate)]
    features['zero_crossing_rate_var'] = [np.var(zero_crossing_rate)]

    y_harmonic, y_percussive = librosa.effects.hpss(audio_file)
    features['harmony_mean'] = [np.mean(y_harmonic)]
    features['harmony_var'] = [np.var(y_harmonic)]
    features['perceptr_mean'] = [np.mean(y_percussive)]
    features['perceptr_var'] = [np.var(y_percussive)]
    
    features['tempo'] = librosa.feature.tempo(y=audio_file, sr = sr)[0]
    
    mfccs = librosa.feature.mfcc(y=audio_file, sr=sr)
    for i, mfcc in enumerate(mfccs):
        features[f'mfcc{i+1}_mean'] = [np.mean(mfcc)]
        features[f'mfcc{i+1}_var'] = [np.var(mfcc)]

    return pd.DataFrame.from_dict(features)

def predict_chunk(model, audio_file, sr):
    """Predict for 3-second audio chunk"""
    data = extract_features(audio_file, sr)
    data = scaler.transform(data)
    pred=model.predict(data)
    return pred[0]

def predict_file(path):
    """Break file into 3-second chunks, predcit for each chunk and select the most frequent answer"""
    # read
    y, sr = librosa.load(path)
    # trim silence
    audio_file, _ = librosa.effects.trim(y)

    
    votes = np.zeros(10)
    
    chunk_len = sr*3 # unit count per 3 seconds
    chunk_count = len(audio_file)//chunk_len
    for chunk_idx in range(chunk_count-1):
        audio_chunk = audio_file[chunk_idx*chunk_len:(chunk_idx+1)*chunk_len]
        label = predict_chunk(model, audio_chunk, sr)
        votes[label] += 1
    last_chunk = audio_file[(chunk_count-1)*chunk_len:]
    label = predict_chunk(model, last_chunk, sr)
    votes[label] += 1
    
    return classes[np.argmax(votes)]