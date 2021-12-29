# Analyse de negation dans ESLO

Le script a été développé pour réaliser l'annotation d’un corpus oral, ESLO. Le corpus est chargé dans un TSV et noté par main s'il y a négation ou pas. Le script principal,  AutoNegation.py, permet d’effectuer une cherche pour déclencheurs et est noté si negation suivi.




## Installation

Dans le dossier zip, vous trouverez les scripts (format py) et des dossiers qui contenant les corpora des étapes différentes.  

_Le dossier principal contient quatre dossiers:_

CorpusCSV - les fichiers finaux lorsque le système a identifié des cas de négation

CorpusTRS - qui contient les fichiers .trs qui peuvent être annotés dans TXM, d’où le fichier XML du corpus doit être placé dans le dossier CorpusXML

CorpusTSV - Les fichiers qui était traiter par CorpusXML_to_TSV.py - le fichier actuellement dedans était traiter par CorpusXML_to_TSV.py et puis annoté par main. Un copie de ce ficher, "copie_ESLO1_ENT_001_C.tsv" , est aussi dans le dossier zip  

CorpusXML - Actuellement contient un fichier annoté dans TXM qui était utilisé pour entraîner le système

_Le fichier principal contient trois fichiers:_
CorpusXML_to_TSV.py - convertir les fichiers qui viennent de TXM à TSV.

AutoNegation.py - le système qui détecte si la négation est présente dans un groupe de souffle. Une évaluation de macro et micro precision, rappel, f-score est automatiquement exécutée à l’étape finale

copie_ESLO1_ENT_001_C.tsv - un copie du fichier annoté dans TXM qui était utilisé pour entraîner le système, au cas où le fichier CorpusXML_to_TSV.py est exécuté




## Requirements

Pour l’exécution du script, il est important d’avoir installé les librairies python suivantes :

* Pandas : https://pandas.pydata.org/docs/getting_started/install.html

* numpy : https://numpy.org/install/

* spacy : https://spacy.io/usage/

* sklearn : https://scikit-learn.org/stable/install.html




## Usage

_Analyser la négation_
-----------

Les fichiers ESLO .trs doivent être chargés dans TXM pour commencer le contrôle des annotations. Les fichiers .tsv qui sont exporté doit ensuite être examiné et des annotations supplémentaires doivent être faites au besoin. Cette étape est actuellement remplacée par l’utilisation du fichier "ESLO1_ENT_001_C.tsv". Un copie de cela est inclus dans le fichier principal s'il y a besoin.

Ensuite, le fichier AutoNegation.py est utilisé. Le système faits des annotations et les exporte à CSV pour les résultats d'être revues. Les measurements de macro et micro precision, rappel, f-score sont exécutées à l’étape finale et sont affichées automatiquement.




## Bugs connus

* _CorpusXML_to_TSV.py_

Le fichier annoté par ce script n'est pas actuellement indique les speakers ni les annotations faites dans TXM, à cause d'un problème non résolu avec Xpath et namespace. La sortie du fichier par le programme doit être entièrement annotée sur TSV dans la colonne negation_control pour que le fichier 2 soit correctement préformé.

Pour éviter temporairement cela, le fichier 'ESLO1_ENT_001_C.tsv' doit être utilisé.   

_AutoNegation.py_
Améliorations de précision nécessaires à la détection de la négation dans les groupes de souffle qui contiennent "n'est-ce pas"

Enrichissement des règles captant la négation nécessaire
