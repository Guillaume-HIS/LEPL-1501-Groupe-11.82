"""
    @author : Groupe 11.82
    @version : 15 novembre 2020

    Ce fichier est le fichier principal de la simulation sont execution cree une fenêtre qui invite l'utilisateur à
    entrer des informations utiles à la simulation concernant la grue en elle-meme
"""


# L'importation ouvre la fenetre
from tkinter_fonctions_simulation import *


# Initialisation de la fenetre (deja ouverte) et recuperation des infos entrees par l'utilisateur dans le tuple inputs
inputs = 0
window_init(wn)
simulation_type = 0
keep_going_home = True
dico_notre_grue = {}
notre_grue = False


class Config_file_error(Exception):
    pass


# Ouvre le fichier notre_grue.config et entre ses valeurs dans un dictionnaire
try:
    with open("notre_grue.config") as file:
        lines = []
        for k in file:
            line = k.replace("\n", "")
            lines.append(line)

        for line in lines:
            elems = line.split(" : ")
            dico_notre_grue[elems[0]] = float(elems[1])

except Exception:
    raise Config_file_error


while keep_going_home:

    inputs = 0

    # La condition est respectee quand on appuie sur back
    while inputs == 0:
        simulation_type = slide0()
        inputs, notre_grue = slide1(simulation_type, dico_notre_grue)

    # Constante de gravitation [m/s**2]
    g = 9.81

    # Variables liées à la plateforme/barge
    lenght = inputs[0]  # Longueur/Largeur de la barge (carré) [m]
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
        m3_1 = inputs[5] + dico_notre_grue["coef_m3"] * inputs[4]
    else:
        m3_1 = inputs[5]  # Masse d'un module [kg]
    m3_2 = inputs[6]
    h1 = inputs[7]  # Hauteur de la barge [m]
    h2 = inputs[8]  # Hauteur totale barge + charge [m]
    masse_vol_milieu = 997

    # Paramètres du système
    # m = m_tot          # masse du bloc [kg]
    # mu = 0.03        # coefficient de frottement visqueux [N*s/m]
    # k = 0.5          # coefficient du ressort [N/m]

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

    # Creation des tableaux contenant les valeus du temps, de l'acceleration, de la vitessse et de l'angle utiles a la
    # creation des graphiques
    t = np.arange(0, end, step)
    x = np.empty_like(t)
    v = np.empty_like(t)
    a = np.empty_like(t)
    y_1 = np.empty_like(t)
    y_2 = np.empty_like(t)
    # lst_i = (x, v, a)
    lst_i = (x, v, a, y_1, y_2)

    # Creation des listes correspondant à le distance en fonction du temps selon le type de simulation
    if d2 is None:
        d = np.full_like(t, d1)
    else:
        d = np.linspace(d1, d2, len(t))

    if m3_2 is None:
        m3 = np.full_like(t, m3_1)
    else:
        m3 = np.linspace(m3_1, m3_2, len(t))

    # On crée un tuple contenant les variables liees à la barge
    infos = (g, h1, h2, lenght, m1, m2, m3, d, masse_vol_milieu)

    # Programme principal
    # lsts_post = simulation(c_i, t, lst_i, infos)
    lsts_post = simulation_static_charge(c_i, t, lst_i, infos)

    if simulation_type == 1:
        keep_going_home = slide_d_static(infos, c_i, t, lsts_post)

    elif simulation_type == 2:
        keep_going_home = slide_d_variable(infos, t)

    elif simulation_type == 3:
        keep_going_home = slide_m_variable()


wn.mainloop()
