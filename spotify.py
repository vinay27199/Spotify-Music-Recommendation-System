import streamlit as st
import pandas as pd
from tqdm import tqdm
import numpy as np

Music_Data=pd.read_csv('/Users/vinaykumarc/Data Science/P180 - Recommendation Engines /Final_Data.csv')
Music_Data['release_date']=Music_Data['release_date'].apply(lambda x:x[:4])
Music_Data['release_date']=pd.to_numeric(Music_Data['release_date'])
Music_Data.dropna(inplace=True)
Music_Data.sort_values(by='release_date',inplace = True)
Music_Data.reset_index(inplace=True)
Music_Data.drop(labels=['index','Unnamed: 0'],axis=1,inplace=True)
songs = Music_Data
st.title('Song Recommender System')
html_temp = """
      <div style="background-color:tomato;padding:10px">
      <h2 style="color:white;text-align:center;"> SONG RECOMMEDER SYSTEM </h2>
      </div>
      """


class spotify_recommender():
    def __init__(self,dataset):
        self.dataset=dataset
    def recommend(self,songs,amount=1):
        distance=[]
        song = self.dataset[(self.dataset.title.str.lower() == songs.lower())].head (1).values[0] 
        rec= self.dataset[self.dataset.title.str.lower() != songs.lower()] 
        for songs in tqdm (rec.values):
            d = 0
            for col in np.arange(len(rec.columns)):
                if not col in [0,1,3,4,18]:
                    d = d + np.absolute (float (song [col]) - float (songs [col]))
            distance.append(d)
        rec['distance'] = distance
        rec = rec.sort_values('distance')
        columns = ['first_artist', 'title','release_date']
        return rec[columns] [: amount]
recommender = spotify_recommender(songs)

def main():

    song = st.text_input("Type your song",)
    result=""
    
    if st.button("Recommend"):
        result=recommender.recommend(song, 10)
        for i in (result['title']):
            st.write(i)
    else:
        print("Song not found")



if __name__=='__main__':
    main()