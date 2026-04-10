Le script `generate.py` permet de générer différentes versions de QCM
sur base d'une banque de questions au format `.xlsx`.

# Requirements

Le script nécessite :
- [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
- [markdown-pdf](https://pypi.org/project/markdown-pdf/)

# Fonctionnement

Le format pour la banque de questions (voir `sample_questions.xlsx`) est le
suivant :
- une colonne `questions` contient le texte de chaque question ;
- les colonnes `A`, `B`, `C`, `D` contiennent jusqu'à 4 propositions de réponse (c'est facilement modifiable si besoin de plus)
- une colonne `category` qui permet d'indiquer les questions redondantes qui ne doivent jamais apparaître dans le même questionnaire (i.e., variantes de questions très proches, ou questions sur un même thème) ;
- une colonne `keep_last` qui doit valoir `TRUE` si la dernière réponse proposée doit toujours apparaître en dernier (et donc ne pas être mélangée avec les autres) (utile pour les réponses comme "Aucune des réponses précédentes").

Le script fonctionne de la façon suivante :
1. tire au hasard **une seule** question par `category` ;
2. tire au hasard $n$ questions parmi les questions tirées au point 1 ;
3. pour chaque question, mélange aléatoirement les réponses (sauf la dernière si `keep_last` est `TRUE`).

Un "scénario" de génération de QCM doit être programmé dans la fonction `main()`
de `generate.py`.

Dans l'exemple (voir `generate.py`), on veut générer 2 versions complétement
différentes par groupe de TP, pour 8 groupes de TP au total, avec 5 questions par QCM.
Le "scénario" s'écrit donc comme ceci :

````python
questions_bank = 'sample-questions.xlsx'
    
output_folder = 'PDF/'

# 8 groups, from 1 to 8
groups = range(1, 9)

for g in groups:
    title = "Le titre de mon QCM"

    # 2 versions per group (A and B)
    generate_mcq(questions_bank=questions_bank,
                 output_filename='PDF/QCM-{0}'.format(g) + 'A',
                 title=title + " ({0}A)".format(g),
                 num_questions=5)
    
    generate_mcq(questions_bank=questions_bank,
                 output_filename='PDF/QCM-{0}'.format(g) + 'B',
                 title=title + " ({0}A)".format(g),
                 num_questions=5)
````

Si l'on veut 2 versions par groupe de TP avec les **mêmes** questions
simplément mélangées, pour 8 groupes de TP au total, avec 5 questions par QCM, il est possible
de récupérer les questions de `generate_mcq()` et de les passer à l'appel suivant comme ci-dessous

````python
questions_bank = 'sample-questions.xlsx'
    
output_folder = 'PDF/'

# 8 groups, from 1 to 8
groups = range(1, 9)

for g in groups:
    title = "Le titre de mon QCM"

    # 2 versions per group (A and B)
    questions = generate_mcq(questions_bank=questions_bank,
                             output_filename='PDF/QCM-{0}'.format(g) + 'A',
                             title=title + " ({0}A)".format(g),
                             num_questions=5)
    
    generate_mcq(questions_bank=questions_bank,
                 output_filename='PDF/QCM-{0}'.format(g) + 'B',
                 title=title + " ({0}A)".format(g),
                 num_questions=5,
                 questions=questions)
````