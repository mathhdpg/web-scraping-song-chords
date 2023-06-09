from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_soup(url):
  print("https://m.cifraclub.com.br" + url)
  webpage = requests.get("https://m.cifraclub.com.br" + url)
  return BeautifulSoup(webpage.content, "html.parser")

def get_song_id(soup):
  id = re.search(r'"music":{"type":"json","json":{"id":(\d+)', str(soup))
  print(id.group(1))
  return id.group(1)

def get_key(soup):
  key = re.search(r'<span>Tom(?:<!--\s-->)?:\s+<b>(.*?)<\/b>', str(soup))
  print("Key -> " + key.group(1))

def get_json_content(soup):
  json = re.search(r'<script>window.__APOLLO_STATE__=({.*})<\/script>', str(soup))
  print(json.group(1))

def get_transpose(id, step):
  url = "https://api.cifraclub.com.br/v3/song/" + str(id) + "/guitar/principal/transpose?halfSteps=" + str(step) + "&newFormat=true"
  print(url)
  webpage = requests.get(url, headers={"Referer": "https://m.cifraclub.com.br/"})
  soup = BeautifulSoup(webpage.content, "html.parser")
  print(soup)

def get_chords(soup):
  chordsContainers = soup.find_all(attrs={"class": "chordWrapper"})
  for x in chordsContainers[0:] :
    chord_div = x.find(attrs = {"class" : "chord" }, recursive = True);
    chord = chord_div.find("strong").get_text()
    chordNotes = chord_div.attrs["data-mount"]
    print(chord + ' - ' + chordNotes)
    
def get_song_chords_in_sequence(soup):
  chords_in_sequence = []
  b = soup.find_all("b")
  for x in b[0:] :
    chords_in_sequence.append(x.get_text())
  return chords_in_sequence

# salva um arquivo txt onde cada item do array corresponde a uma linha no arquivo. 
def salva_array_em_txt(path, array):
  with open(path, "w") as arquivo:
    for texto in array:
      arquivo.write(texto + "\n");  

webpage = requests.get("https://m.cifraclub.com.br/djavan/musicas.html")
soup = BeautifulSoup(webpage.content, "html.parser")

ul = soup.find_all(attrs={"id": "artist-top-musics"})
for x in ul[0:] :
  lis = x.find_all("li")
  for li in lis[1:] :
    url = li.find("a").attrs["href"]
    if (not url.endswith("/letra/")):
      try:
        print(url)
        soup = get_soup(url)
        #id = get_song_id(soup)

        #get_json_content(soup)
        get_key(soup)
        #get_chords(soup)
        chords_in_sequence = get_song_chords_in_sequence(soup)
        salva_array_em_txt("dataset" + url[:-1] + ".txt", chords_in_sequence)
#        for  step in range(1, 12):
#          get_transpose(id, step)
      except:
        print("########## ERRO PROCESSANDO " + url)