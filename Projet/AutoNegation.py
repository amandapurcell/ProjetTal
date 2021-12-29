import re
import os
from numpy import complexfloating
import spacy
import pandas as pd
from spacy.util import join_command
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support


# Listes 
templist = []
negation_list = []
negation_trouve = []
groupsouffle_liste = []
compt_neg = 0
cols = ["group_souffle", "negation_control","negation"]

nlp = spacy.load("fr_core_news_lg")

# Les chemins 
path=r"./CorpusTSV/"
outPath= r"./CorpusCSV/"

# Trouver les fichiers
directory = os.listdir(path)

for f in directory:
    fichierNom = f
    fichierNomSortie = re.sub('\.tsv', '.csv', fichierNom)
# Ouvrir les fichiers
fichier = pd.read_csv( os.path.join(path, f),usecols = cols, sep='\t')

groupsouffle = fichier['group_souffle'].tolist()

# convertir la liste à itérateur
iterator_gs = iter(groupsouffle)

for ligne in iterator_gs:
    doc= nlp(ligne)
    negation_temp = []
    compt_neg = 0
   
   #Identifier la négation
    try:
        for token in doc:

            try: 
                # Ne. . . pas
                if token.lower_ == "ne": 
                    if token.nbor().text == "pas":
                        if token.nbor().nbor().pos_ in ("VERB","AUX"): #ne pas VERB
                            negation_temp.append(token.text+ " "+token.nbor().text + " " + token.nbor().nbor().text)
                            compt_neg +=1
                        #ne + VERB + pas
                    elif token.nbor().pos_ in ("VERB","AUX"):
                        if token.nbor().nbor().text == "pas":
                            negation_temp.append(token.text+ " "+token.nbor().text + " " + token.nbor().nbor().text)
                            compt_neg +=1
                        elif token.nbor().nbor().text == "plus": #ne + VERB + plus
                            negation_temp.append(token.text+ " "+token.nbor().text + " " + token.nbor().nbor().text)
                            compt_neg +=1
                elif token.lower_ =="n": # répétition pour "n'"
                    if token.nbor().text =="'":
                        if token.nbor().nbor().pos_ in ("VERB","AUX"):
                            if token.nbor().nbor().nbor().text == "pas": #n' + VERB + pas
                                negation_temp.append(token.text+ " "+token.nbor().text + " " + token.nbor().nbor().text)
                                compt_neg +=1
                            if token.nbor().nbor().nbor().text == "plus": #n' + VERB + plus
                                negation_temp.append(token.text+ " "+token.nbor().text + " " + token.nbor().nbor().text)
                                compt_neg +=1
                            elif token.nbor().nbor().nbor().text == "-ce": #n'est-ce pas
                                if token.nbor().nbor().nbor().nbor().text == "pas":
                                    negation_temp.append(token.text+token.nbor().text + token.nbor().nbor().text + token.nbor().nbor().nbor().text + " "+ token.nbor().nbor().nbor().nbor().text)
                                    compt_neg +=1
                elif token.lower_ != "ne": # répétition pour les cas sans 'ne'
                    if token.nbor().pos_ in ("VERB", "AUX"): 
                        if token.nbor().nbor().text == "pas": # VERB + pas
                            negation_temp.append(token.nbor().text+ " "+token.nbor().nbor().text)
                            compt_neg +=1
                        elif token.nbor().nbor().text == "plus": # VERB + plus
                            negation_temp.append(token.nbor().text+ " "+token.nbor().nbor().text)
                            compt_neg +=1
                        # elif token.n$
                        elif token.nbor().nbor().text == "jamais": # VERB + jamais
                            negation_temp.append(token.nbor().text+ " "+token.nbor().nbor().text)
                            compt_neg +=1
                        elif token.nbor().nbor().text == "personne": # VERB + personne
                            negation_temp.append(token.nbor().text+ " "+token.nbor().nbor().text)
                            compt_neg +=1
                    elif token.is_sent_start == "true": # répétition pour les cas sans 'ne' ou le verbe commence la ligne
                        if token.pos_ in ("VERB", "AUX"): 
                            if token.nbor().text == "pas": # VERB + pas
                                negation_temp.append(token.text+ " "+token.nbor().text)
                                compt_neg +=1
                            elif token.nbor().text == "plus": # VERB + plus
                                negation_temp.append(token.text+ " "+token.nbor().text)
                                compt_neg +=1
                            # elif token.n$
                            elif token.nbor().text == "jamais": # VERB + jamais
                                negation_temp.append(token.text+ " "+token.nbor().text)
                                compt_neg +=1
                            elif token.nbor().text == "personne": # VERB + personne
                                negation_temp.append(token.text+ " "+token.nbor().text)
                                compt_neg +=1
                    
                       
            except IndexError:
                dernier_tok = token.text 
                if len(negation_temp) >= 1 :
                    negation_trouve.append(negation_temp)
                else:
                    negation_trouve.append("o")
                if compt_neg >=1:
                    negation_list.append("V")
                else:
                    negation_list.append("F")
                

                
                   
                try:
                    nextline = next(iterator_gs)
                    ligne2 = []
                    negation_temp = []
                    compt_neg = 0
                    
                    mots2= ''
                    for replacement_neighbor in nextline.split():
                        ligne2.append(replacement_neighbor) #itérateur à liste
                        mots2=' '.join(ligne2) # liste à chaîne

                        doc2= nlp(mots2)
                 
                    for token in doc2:
                        try: 
                            # Ne. . . pas
                            if dernier_tok == "ne":
                                if token.text == "pas":
                                    if token.nbor().pos_ in ("VERB","AUX"): #ne pas VERB
                                            negation_temp.append(dernier_tok + " "+ token.text+ " "+token.nbor().text)
                                            compt_neg +=1
                                #ne + VERB + pas
                                elif token.is_sent_start == "true":
                                    if token.pos_ == "VERB": 
                                        if token.nbor().text == "pas":
                                            negation_temp.append(dernier_tok+ " " +token.text+ " "+token.nbor().text)
                                            compt_neg +=1
                                        if token.nbor().text == "plus": #ne + VERB + plus
                                            negation_temp.append(dernier_tok+ " " + token.text+ " "+token.nbor().text)
                                            compt_neg +=1
                                # Traiter les tokens qui viennent après le déclencheur qui a provoqué une error, mais où la derniere ligne se termine par 'ne'
                                elif token.pos_ == "VERB": 
                                        if token.nbor().text == "pas": #VERB + pas
                                            negation_temp.append(token.text+ " "+token.nbor().text)
                                            compt_neg +=1
                                        if token.nbor().text == "plus": #VERB + plus
                                            negation_temp.append(token.text+ " "+token.nbor().text)
                                            compt_neg +=1

                            else: # Traiter les tokens qui viennent après le déclencheur qui a provoqué une error
                                if dernier_tok != "ne": 
                                    if token.pos_ == "VERB": #VERB + pas
                                        if token.nbor().text == "pas":
                                            negation_temp.append(token.text+ " "+token.nbor().text)
                                            compt_neg +=1
                                        elif token.nbor().text == "plus": #VERB + plus
                                            negation_temp.append(token.text+ " "+token.nbor().text)
                                            compt_neg +=1
                                        elif token.nbor().text in ("aucune","aucunes","aucun", "aucuns"): # VERB + aucune
                                            negation_temp.append(token.text+ " "+token.nbor().text)
                                            compt_neg +=1
                                        elif token.nbor().text == "jamais": # VERB + jamais
                                            negation_temp.append(token.text+ " "+token.nbor().text)
                                            compt_neg +=1
                                        elif token.nbor().text == "personne": # VERB + personne
                                            negation_temp.append(token.text+ " "+token.nbor().text)
                                            compt_neg +=1
                        
                                

                            if token.lower_ =="n": #Répétition pour "n'"
                                if len(doc2) >= 7:  # Verifier que ce n'est pas le seule chose dans le group de souffle
                                    if token.nbor().text =="'":
                                                if token.nbor().nbor().pos_ in ("VERB","AUX"):
                                                    if token.nbor().nbor().nbor().text == "-ce": #n'est-ce pas
                                                        if token.nbor().nbor().nbor().nbor().text == "pas":
                                                            negation_temp.append(token.text+token.nbor().text + token.nbor().nbor().text + token.nbor().nbor().nbor().text + " "+ token.nbor().nbor().nbor().nbor().text)
                                                            compt_neg +=1
                            elif token.is_sent_start == "true": # répétition pour les cas sans 'ne' ou le verbe commence la ligne 
                                if token.pos_ in ("VERB", "AUX"): 
                                    if token.nbor().text == "pas": # VERB + pas
                                        negation_temp.append(token.text+ " "+token.nbor().text)
                                        compt_neg +=1
                                    elif token.nbor().text == "plus": # VERB + plus
                                        negation_temp.append(token.text+ " "+token.nbor().text)
                                        compt_neg +=1
                                    # elif token.n$
                                    elif token.nbor().text == "jamais": # VERB + jamais
                                        negation_temp.append(token.text+ " "+token.nbor().text)
                                        compt_neg +=1
                                    elif token.nbor().text == "personne": # VERB + personne
                                        negation_temp.append(token.text+ " "+token.nbor().text)
                                        compt_neg +=1
                        except:
                            pass
                except IndexError:
                    pass
                pass
        if len(negation_temp) >= 1 :
            negation_trouve.append(negation_temp)
        else:
            negation_trouve.append("o")
        if compt_neg >=1:
            negation_list.append("V")
        else:
            negation_list.append("F")

        negation_temp = []
        compt_neg = 0

    except StopIteration:
        pass

#  Faire des colonnes pour la négation du système en csv
fichier['negation trouvé'] = negation_trouve
fichier['negation'] = negation_list 
     

# Ecrire les fichiers
fichier.to_csv(outPath + fichierNomSortie, index = False)


# Resultats

print("\n Les infos (macro : precision, rappel, fscore)) de scikit pour le fichier : " ,fichierNom, "sont : ", precision_recall_fscore_support(
    fichier['negation_control'], fichier['negation'], average='macro',
))
print("\n Les infos (micro : precision, rappel, fscore) de scikit pour le fichier : ",fichierNom, "sont : ", precision_recall_fscore_support(
    fichier['negation_control'], fichier['negation'], average='micro'
))