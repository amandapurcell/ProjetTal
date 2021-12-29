from typing import Text
import xml.etree.ElementTree as ET
import os
import re
import numpy
import pandas as pd

# Listes 
groupsouffle = []
mots= []
negation =[]
speaker = []
compt_neg = 0

cols = ["group_souffle","speaker", "negation_control","negation"]

# Les chemins 
path=r"./CorpusXML/"
outPath= r"./CorpusTSV/"

directory = os.listdir(path)

for fichierNom in directory:
    fichierNomSortie = re.sub('\.xml', '.tsv', fichierNom)

# Ouvrir les fichiers
try :
    tree = ET.parse(path+fichierNom)
except IOError:
    print ("le fichier n'existe pas")
except etree.XMLSyntaxError:
    print ("le fichier n'est pas au format xml")
else:
    root = tree.getroot()

    for u in root.iter("{http://www.tei-c.org/ns/1.0}u"): # trouver les groupes de souffle

        # for speak in root.iter("{http://www.tei-c.org/ns/1.0}u[@spk]"): #trouver les speakers
        # for neg_annote in u.iter("{http://textometrie.org/1.0}type="\#negation"): #trouver les annotations
        #     if xxxx contains: #find if negation
        #         compt_neg += 1    
        

        for motform in u.iter("{http://textometrie.org/1.0}form"): # trouver les mots
            mots.append(motform.text) #ajouter les mots à la liste des mots
        if len(mots) >=1:
            mots2=' '.join(mots)
            groupsouffle.append(mots2) #faire la liste de chaines

            speaker.append(" ") #changer quand l'attribute est trouvé
            negation.append(" ") #changer quand l'attribute est trouvé
            
    
            mots = []#refire la liste
            mots2 =""
        # 
    

df = pd.DataFrame(columns = ["group_souffle","speaker", "negation_control","negation"]) # Définir le Dataframe et les colonnes
df['group_souffle'] = groupsouffle 
df['speaker'] = speaker
df['negation_control'] = negation

#Ecrire TSV
df.to_csv(outPath + fichierNomSortie,index=False, sep="\t")
# fichier = pd.read_csv( os.path.join(path, f),usecols = cols, sep='\t')


print("fini")