# LEPL-1501 : Groupe-11.82

Ce programme est le programme de simulation du projet 1 (LEPL-1501) du groupe 11.82.

<img src="https://github.com/Guillaume-HIS/LEPL-1501-Groupe-11.82/blob/main/logo.png?raw=true" width=150>

### Auteurs :
  - Guillaume HISETTE
  - Hippolyte HILGERS
  - Lancelot HEYMANS
  - Aurélien HERMANT
  - Antoine HOCHART
  - François HOLOGNE

### Tuteur du projet:
  - Hadrien LIBIOULLE

---

## Utilisation

### Modules python requis :
  - PIL pour le traitement et l'affichage des images (attention pas installé de base)
  - tkinter pour la gestion de l'interface graphique
  - matplotlib pour l'affichage des graphiques
  - numpy
  
### Exécution

Le programme est séparé en trois fichiers de code : 
  - main_simulation.py
  - tkinter_fonctions_simulation.py
  - fonctions_math_simulation.py

Pour executer le programme, il faut executer le fichier main_simulation.py

### Fichier config

Le fichier config contient 7 éléments :
  - largeur : x où x représente la largeur/longueur de la barge carrée
  - m1 : x où x représente la masse de la barge
  - m2 : x où x représente la masse de la grue qui est placée sur la barge
  - h1 : x où x représente la hauteur de la barge
  - h2 : x où x représente la hauteur à laquelle la grue est placée sur la barge
  - coef_m3 : x où x représente un coefficient qui a été calculé par essai/erreur avec les mesures d'angles effectuées
  - moment_inertie : x où x représente le moment d'inertie du système sur son axe d'oscillation

### Problèmes connus

Si vous eprouver des difficultes avec le fichier notre_grue.config ou recevez des erreurs
du type Config_file_error, le programme peut toujours fonctionner sans les donnees de notre grue et donc en
fonctionnant tel que decrit dans l'exercice de physique 2.
Pour ce faire il suffit de modifier la ligne 53 du fichier main_simulation.py: 
~~~python
dico_notre_grue = open_config_file()
~~~
par 
~~~python
dico_notre_grue = {}
~~~
et de ne pas cliquer sur le bouton notre grue lors de l'execution

