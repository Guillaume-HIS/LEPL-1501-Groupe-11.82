"""
    @author : Groupe 11.82
    @version : 15 novembre 2020

    Ce fichier est le fichier principal de la simulation sont execution cree une fenêtre qui invite l'utilisateur à
    entrer des informations utiles à la simulation concernant la grue en elle-meme

    Modules necessaires : PIL, numpy, matplotlib, tkinter

    NB : Si vous eprouver des difficultes avec le fichier notre_grue.config ou recevez des erreurs
    du type Config_file_error, le programme peut toujours fonctionner sans les donnees de notre grue et donc en
    fonctionnant tel que decrit dans l'exercice de physique 2.
    Pour ce faire il suffit de modifier la ligne 53 : dico_notre_grue = open_config_file() par dico_notre_grue = {}
    et de ne pas cliquer sur le bouton notre grue lors de l'execution
"""


# L'importation ouvre la fenetre
from tkinter_fonctions_simulation import *


def open_config_file(filename="notre_grue.config"):
    class Config_file_error(Exception):
        """
        Classe d'erreur qui est appelée lorsque le fichier notre_grue.config n'est pas trouve ou que les
        infos s'y trouvant ne correspondent pas a ce qui est attendu
        """
        pass

    # Ouvre le fichier notre_grue.config et entre ses valeurs dans un dictionnaire
    dico = {}
    try:
        with open(filename) as file:
            lines = []
            for k in file:
                line = k.replace("\n", "")
                lines.append(line)

            for line in lines:
                elems = line.split(" : ")
                dico[elems[0]] = float(elems[1])

            return dico
    except Exception:
        raise Config_file_error


# Initialisation de la fenetre (deja ouverte) et initialisation d'un certain nombre de variable
inputs = 0
window_init(wn)
simulation_type = 0
keep_going_home = True
dico_notre_grue = open_config_file()
notre_grue = False


# La condition est toujours respectée tant qu'un appuie sur HOME, elle ne l'est plus si on ferme la fenetre lors de
# l'affichage d'un des slide2
while keep_going_home:

    inputs = 0

    # La condition est respectee tant qu'on appuie sur back
    while inputs == 0:

        simulation_type = slide0()
        # Si simulation_type = None, cad si la fenetre gets ete fermee sur slide0, on break la boucle
        if simulation_type is None:
            break

        inputs, notre_grue = slide1(simulation_type, dico_notre_grue)
        # Si inputs = 1, cad si la fenetre gets ete fermee sur slide1, on break la boucle
        if inputs == 1:
            break

    # Constante de gravitation [m/s**2]
    g = 9.81


    # Variables liées à la plateforme/barge

    # Si inputs n'est pas un tuple, cad si la fenetre gets ete fermee, on break la boucle
    try:
        lenght = inputs[0]  # Longueur/Largeur de la barge (carrée) [m]
    except TypeError:
        break

    if notre_grue:
        d1 = inputs[1] + dico_notre_grue["largeur"] / 2
    else:
        d1 = inputs[1]  # Distance de déplacement de depart d'un module [m]
    d2 = inputs[2]  # Distance de déplacement finale d'un module [m]
    m1 = inputs[3]  # Masse de la barge [kg]
    if notre_grue:
        m2 = inputs[4] * (1 - dico_notre_grue["coef_m3"])
    else:
        m2 = inputs[4]  # Masse de la charge totale [kg]
    if notre_grue:
        m3 = inputs[5] + dico_notre_grue["coef_m3"] * inputs[4]
    else:
        m3 = inputs[5]  # Masse d'un module [kg]
    h1 = inputs[7]  # Hauteur de la barge [m]
    h2 = inputs[8]  # Hauteur totale barge + charge [m]
    masse_vol_milieu = 997

    # Paramètres de la simulation
    step = 0.001     # pas (dt) [s]
    end = 10       # durée [s]
    x_0 = 0.000000001  # angle d'inclinaison initial [radian]
    v_0 = 0  # vitesse angulaire initiale [radian/s]
    inertia = 7.95  # moment d'inertie total [N*m ou kg*m^2*s^2]
    D = 10.0  # coefficient d'amortissement total [N*m*s]
    # rot_in = 50
    # c_i = (x_0, v_0, k, mu, m, rot_in, step)
    c_i = (x_0, v_0, inertia, D, step)

    # Creation des tableaux contenant les valeus du temps, de l'acceleration, de la vitessse et de l'angle utiles gets la
    # creation des graphiques
    t = np.arange(0, end, step)
    x = np.empty_like(t)
    v = np.empty_like(t)
    a = np.empty_like(t)
    y_1 = np.empty_like(t)
    y_2 = np.empty_like(t)
    lst_i = (x, v, a, y_1, y_2)


    # Creation des listes correspondant à le distance en fonction du temps selon le type de simulation
    if d2 is None:
        d = np.full_like(t, d1)
    else:
        d = np.linspace(d1, d2, len(t))


    # On crée un tuple contenant les variables liees à la barge
    infos = (g, h1, h2, lenght, m1, m2, m3, d, masse_vol_milieu)


    # Programme de simulation
    lsts_post = simulation_static_charge(c_i, t, lst_i, infos)

    if simulation_type == 1:
        keep_going_home = slide_d_static(infos, c_i, t, lsts_post)

    elif simulation_type == 2:
        keep_going_home = slide_d_variable(infos, t)


wn.destroy()
