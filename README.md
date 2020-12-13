# LEPL-1501 : Groupe-11.82

Ce programme est le programme de simulation du projet 1 (LEPL-1501) du groupe 11.82.

### Auteurs :
  - Guillaume HISETTE
  - Hippolyte HILGERS
  - Lancelot HEYMMANS
  - Aurélien HERMANT
  - Antoine HOCHART
  - François HOLOGNE

### Tuteur du projet:
  - Hadrien LIBIOULLE


## Utilisation

### Modules python requis :
  - PIL pour le traitement et l'affichage des images (attention pas installé de base)
  - tkinter pour la gestion de l'interface graphique
  - matplotlib pour l'affichage des graphiques
  - numpy
  
### Execution

Le programme est séparé en trois fichiers de code : 
  - main_simulation.py
  - tkinter_fonctions_simulation.py
  - fonctions_math_simulation.py

Pour executer le programme, il faut executer le fichier main_simulation.py

### Problèmes connus

Si vous eprouver des difficultes avec le fichier notre_grue.config ou recevez des erreurs
du type Config_file_error, le programme peut toujours fonctionner sans les donnees de notre grue et donc en
fonctionnant tel que decrit dans l'exercice de physique 2.
Pour ce faire il suffit de modifier la ligne 53 : 
~~~python
dico_notre_grue = open_config_file()
~~~
par 
~~~python
dico_notre_grue = {}
~~~
et de ne pas cliquer sur le bouton notre grue lors de l'execution
