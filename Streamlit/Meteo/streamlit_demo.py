import json, requests, datetime,os
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from joblib import dump
from meteo_ML import * 
import streamlit as st 

cities = ['paris', 'london', 'washington']
requests_weather = [load_weather_data(city) for city in cities]


with open(f'./raw_files/{datetime.datetime.now().timestamp()}.json', 'w') as f:
    json.dump(requests_weather, f)

#transform_data_into_csv()
transform_data_into_csv(filename='fulldata.csv')
X, y = prepare_data('./clean_data/fulldata.csv')

df = pd.read_csv("./clean_data/fulldata.csv")


st.sidebar.title("Différents Onglets")
page = st.sidebar.radio("Choisir une page",["Presentation","Presentation jeu de données","Visualisation","Modelisation"])


if page == "Presentation":
    st.title("Titre du Projet")
    st.header("Thème du projet")
    st.image('https://openweathermap.org/themes/openweathermap/assets/img/logo_white_cropped.png')
    city_user = st.selectbox("Choisir une ville" ,cities)
    
    st.write(load_weather_data(city_user ))

    st.write(load_weather_data(city_user ).keys())

    st.markdown("ceci est un [lien](https://www.meteomatics.com/en/api/getting-started/?ppc_keyword=api%20openweathermap&gclid=CjwKCAiA5sieBhBnEiwAR9oh2iahus0RKRUKRPEheJulMeeMA3ZSoOhDu19QMOPEA0Y9kTEhP1X35RoCgzwQAvD_BwE)")
if page == "Visualisation":
    import seaborn as sns 
    import matplotlib.pyplot as plt
    fig = plt.figure()
    sns.scatterplot(df["temperature"], df["pression"],df["city"])
    st.pyplot(fig )


if page == "Modelisation":
    
    score_lr = compute_model_score(LinearRegression(), X, y)
    score_dt = compute_model_score(DecisionTreeRegressor(), X, y)
    score_rf = compute_model_score(RandomForestRegressor(), X, y)
    dict_cross_val_score={'lr':score_lr,'dt':score_dt,'rf':score_rf}
    model_utilisateur = st.selectbox("Choisir un modèle classification",dict_cross_val_score.keys())
    st.write(dict_cross_val_score[model_utilisateur ])
    
    print(dict_cross_val_score)
if page == "Presentation jeu de données":
    st.button("Cliquer sur le bouton")
    st.video("https://www.youtube.com/watch?v=nGVoHEZojiQ")

    