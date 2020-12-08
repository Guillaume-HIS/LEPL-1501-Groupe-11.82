"""
    @author : Groupe 11.82
    @version : 15 novembre 2020

    Ce fichier contient les fonctions qui s'occupent concretement de la simulation
"""


import math
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def enfoncement(rho, length, masse_tot):
    """
    :param masse_tot: m1 + m2
    :param rho: Masse volumique du liquide (en kg/m³)
    :param length: Largeur de la barge, supposée carrée, (en m)
    :return: la hauteur d'enfoncement de la barge (en m)
    """
    hc = masse_tot/(rho*(length**2))
    return hc


def p_archi(g, m):
    """

    :param g: constante de gravite
    :param m: Une masse en Kg
    :return: La Poussé d'archimède , (en N),exercée par le liquide sur length'objet pour autant que celui ci flotte
    """
    p = m*g
    return p


def position_cg_init(hc, dico_situation_elem):
    """

    :param hc: La hauteur d'enfoncement de la plateforme
    :param dico_situation_elem: Un dictionnaire avec en clé la masse de chaque élément du système, et en valeur une
                                liste de deux coordonées, en premier la position en x de length'élément par rapport
                                au centre de la barge, et en deuxième la position en y de length'élément par rapport
                                 au bas de la barge
    :return:
    """
    x = 0
    y = 0
    m = 0
    for masse in dico_situation_elem:
        x += dico_situation_elem[masse][0] * masse
        y += dico_situation_elem[masse][1] * masse
        m += int(masse)
    x = x/m
    y = (y/m) - hc
    return x, y


def position_cp_init(hc):
    """
    :param hc: La hauteur d'enfoncement de la plateforme
    :return: La position initiale du centre de poussée
    """
    return 0, (-hc/2)


def theta_max(h1, hc, length):
    """
    :param h1: La hauteur de la barge (en m)
    :param hc: La hautteur d'enfoncement de la barge (en m)
    :param length: La largeur de la barge, supposée carrée, (en m)
    :return: L'angle de rotation maximal que la plateforme peut subir
    """
    submersion = math.atan((h1 - hc) / (length / 2))
    soulevement = math.atan(hc / (length / 2))
    return submersion, soulevement


def position_cg_rota(xg, yg, theta):
    """
    :param xg:
    :param yg:
    :param theta: un certain angle (en rad)
    :return: La nouvelle position du centre de gravité en fonction de la valeur de length'angle théta
    """

    x2 = math.cos(theta) * xg - math.sin(theta) * yg
    y2 = math.cos(theta) * yg + math.cos(theta) * xg

    return x2, y2


def position_cp_rota(theta, length, hc):
    """
    :param theta: un certain angle (en rad)
    :param length: La largeur de la barge, supposée carrée, (en m)
    :param hc: La hautteur d'enfoncement de la barge (en m)
    :return: La nouvelle position du centre de gravité en fonction de la valeur de length'angle théta
    """

    h_inclin = (length / 2) * math.tan(theta)
    h_1 = hc+h_inclin
    h_2 = hc - h_inclin
    l_trap = length * (h_1 + 2 * h_2) / (3 * (h_1 + h_2))
    h_trap = (h_1**2 + h_1 * h_2 + h_2**2)/(3*(h_1+h_2))
    a = (length / 2) - l_trap
    b = h_trap - hc
    return math.cos(theta)*a - math.sin(theta)*b, math.cos(theta)*b + math.sin(theta)*a


def couple_redressement(xc, xg, g, m):
    """
    :param: une masse en kg
    :return:le couple de redressement du système
    """

    return (xc-xg) * p_archi(g, m)  # a voir


def couple_chavirement(g, m, d):
    """
    :param g: constante de gravite
    :param m: La masse de length'object déplacé
    :param d: La distance horizontale à laquelle on déplace length'object
    :return: Le couple de chavirage
    """
    return m*d*g


def recherche_theta(info):
    """
    Cette fonction chercherche par essai/erreur avec un algorythme de recherche dichotomique l'angle de stabilite
    theta du systeme avec une precision de 10**(-5) radians

    :param info: un tuple contenant les informations nécessaires à la recherche
    :return: un tuple contenant l'angle de stabilite theta en radian et en degres
    """

    g, h1, h2, l, m1, m2, m3_l, d, rho = info
    m_tot = m1 + m2

    try:
        m3 = m3_l[0]
    except IndexError:
        m3 = m3_l

    try:
        dist = d[0]
    except IndexError:
        dist = d

    found = False
    angle_max = math.pi / 2
    angle_min = 0
    theta = (angle_max + angle_min) / 2  # Angle d'inclinaison
    theta_degres = theta * 180 / math.pi  # Angle d'inclinaison en degres
    dico = {m1: [0, h1/2], m2: [0, (h1+h2)]}

    while not found:

        hc = enfoncement(rho, 1, m_tot)
        xcg = position_cg_init(hc, dico)[0]
        ycg = position_cg_init(hc, dico)[1]
        cg_x, cg_y = position_cg_rota(xcg, ycg, theta)
        cp_x, cp_y = position_cp_rota(theta, l, hc)
        cr = couple_redressement(cp_x, cg_x, g, m_tot)  # Couple de redressement [N/m]
        ci = couple_chavirement(g, m3, dist)   # Couple d'inclinaison [N/m]

        # Recherche dichotomique
        if abs(abs(cr) - abs(ci)) < 10**(-5):
            found = True
        elif abs(cr) < abs(ci):
            angle_min = theta
            theta = (angle_min + angle_max)/2
        elif abs(cr) > abs(ci):
            angle_max = theta
            theta = (angle_min+angle_max)/2

        theta_degres = theta * 180/math.pi

    return theta, theta_degres


def simulation(c_init, t, lst_init, infos):
    """
    pre: -
    post: exécute une simulation jusqu'à t=end par pas de dt=step.
          Remplit les listes x, v, a des positions, vitesses et accélérations.
    """

    # conditions initiales
    g, h1, h2, lenght, m1, m2, m3_l, d1, masse_vol_milieu = infos
    # TODO !!!! m3[0]
    m3 = m3_l[0]
    x_0, v_0, k, mu, rot_inert, step = c_init
    x, v, a = lst_init
    m_tot = m1 + m2 + m3
    dico = {m1: [0, h1 / 2], m2: [0, (h1 + h2)]}
    hc = enfoncement(masse_vol_milieu, lenght, m_tot)

    x[0] = x_0
    v[0] = v_0

    for i in range(len(t) - 1):
        dt = step

        # calcul de la force totale
        c_chavirement = couple_chavirement(g, m3, d1)
        c_redressement = couple_redressement(position_cp_rota(x[i], lenght, hc)[0],
                                             position_cg_rota(position_cg_init(hc, dico)[0],
                                                              position_cg_init(hc, dico)[1], x[i])[0], g, m_tot)

        c_tot = c_chavirement + c_redressement

        # calcul accélération, vitesse, position
        a[i] = c_tot / rot_inert
        v[i + 1] = v[i] + a[i] * dt
        x[i + 1] = x[i] + v[i] * dt
        a[i + 1] = a[i]

    return x, v, a


def evolution_cg(x_0, z_0, theta_evo):
    """
    Retourne la position horizontale de centre de poussee a un certain angle

    :param x_0: position initiale du centre de gravite sur l'axe X
    :param z_0: position initiale du centre de gravite sur l'axe Y
    :param theta_evo: angle d'inclinaison auquel on veut connaitre la position du centre de gravite

    :return: la position du centre de gravite sur l'axe X quand le systeme est incline d'un angle theta_evo
    """

    theta_g = math.atan(z_0 / x_0)
    d_0_cg = math.sqrt(x_0 ** 2 + z_0 ** 2)  # distance entre l'origine du repère et le Centre de gravité
    x_g = d_0_cg * math.sin(theta_evo + theta_g)  # position du centre de gravité selon l'axe X

    return x_g


def evolution_cp(hc, length, theta_evo):
    """
    Retourne la position horizontale de centre de poussee a un certain angle

    :param hc: enfoncement de la barge [m]
    :param length: largeur de la barge supposee carree [m]
    :param theta_evo: angle d'inclinaison auquel on veut connaitre la position du centre de poussee

    :return: position du centre de poussee sur l'axe X
    """

    down_side = hc - (length / 2) * (math.tan(theta_evo))
    up_side = hc + (length / 2) * (math.tan(theta_evo))
    x_flott = length / 2 - (length / 3) * ((2 * down_side + up_side) / (down_side + up_side))
    z_flott = hc - (down_side ** 2 + down_side * up_side + up_side ** 2) / (3 * (down_side + up_side))
    theta_c = math.atan(z_flott / x_flott)
    d_0_cc = math.sqrt(x_flott ** 2 + z_flott ** 2)  # distance entre l'origine du repère et le Centre de poussée
    x_c = d_0_cc * math.cos(theta_evo + theta_c)  # position du centre de poussée selon l'axe X

    return x_c


def simulation_static_charge(c_init, t, lst_init, infos):
    """
    pre: -
    post: exécute une simulation jusqu'à t=end par pas de dt=step.
          Remplit les listes theta, w, a_w des angles, vitesses angulaires et accélérations angulaires.
    """
    g, h1, h2, l, m1, m2, m3, d, rho = infos
    theta, w, a_w, y_1, y_2 = lst_init
    theta_0, w_0, I, D, step = c_init
    # Variables
    # TODO !!!! m3[0]
    m_tot = m1 + m2 + m3[0]
    # dico_situation_elem = {m1: [0, h1/2], m2: [0, h1+h2], m3: [d1, h1+h2]}

    # Paramètres du système
    hc = enfoncement(rho, l, m_tot)  # hauteur de la ligne de flottaison [m]
    fg = m_tot * g
    fa = p_archi(g, m_tot)

    # Conditions initiales
    theta[0] = theta_0
    w[0] = w_0
    y_1[0] = theta_max(h1, hc, l)[0]
    y_2[0] = -(y_1[0])
#     x_0, z_0 = position_cg_init(hc, dico_situation_elem) # Référence aux exercices de phyisique Inclinaison et couple,
# #                                                           position du centre de gravité selon l'axe X et l'axe Z

    dt = step

    for i in range(len(t) - 1):
        y_1[i + 1] = y_1[i]
        y_2[i + 1] = y_2[i]

        dico_situation_elem = {m1: [0, h1 / 2], m2: [0, h1 + h2], m3[i]: [d[i], h1 + h2]}
        x_0, z_0 = position_cg_init(hc, dico_situation_elem)

        x_g = evolution_cg(x_0, z_0, theta[i])
        x_c = evolution_cp(hc, l, theta[i])

        # calcul de l'accélération angulaire, vitesse angulaire et angle
        a_w[i] = (fg * x_g - fa * x_c - D * w[i]) / I
        theta[i + 1] = theta[i] + w[i] * dt
        w[i + 1] = w[i] + a_w[i] * dt
        a_w[i + 1] = a_w[i]

    return theta, w, a_w, y_1, y_2


def change_subplot_color(subplot, bg, axis):

    subplot.set_facecolor(bg)
    subplot.spines['bottom'].set_color(axis)
    subplot.spines['top'].set_color(axis)
    subplot.spines['right'].set_color(axis)
    subplot.spines['left'].set_color(axis)
    subplot.tick_params(axis="x", colors=axis, which="both")
    subplot.tick_params(axis="y", colors=axis, which="both")
    subplot.title.set_color(axis)
    subplot.yaxis.label.set_color(axis)
    subplot.xaxis.label.set_color(axis)


def graphiques(wind, t, lsts_pst):
    """
    Affiche une Figure contenant 3 graphiques : angle, vitesse angulaire et acceleration angulaire p/r au temps

    :param wind: fenetre dans laquelle les graphiques doivent s'afficher
    :param t: tableau des temps
    :param lsts_pst: tuple contenant les listes x, v et a representant respectivement l'angle d'inclinaison, la vitesse
                       angulaire et l'acceleration angulaire par rapport au temps

    :return: -
    """

    x, v, a_w, y_1, y_2 = lsts_pst

    fig1 = Figure(figsize=(7, 7))
    fig1.subplots_adjust(hspace=1)
    fig1.patch.set_facecolor("#3c3f41")

    # Creation du subplot a qui represente l'angle
    a = fig1.add_subplot(3, 1, 1)
    a.set_title("Postition p/r au temps")
    a.plot(t, x, label="x")
    a.plot(t, y_2, "r", label="Theta max")
    a.plot(t, y_1, "r")
    a.legend(loc="upper right")
    a.set_xlabel("Temps (s)")
    a.set_ylabel("Angle d'inclinaison (rad)")
    # Changement des couleurs de a
    change_subplot_color(a, "#3c3f41", "w")

    # Creation du subplot b qui represente la vitesse angulaire
    b = fig1.add_subplot(3, 1, 2)
    b.set_title("Vitesse angulaire p/r au temps")
    b.plot(t, v, label="\u03C9")
    b.legend()
    b.set_xlabel("Temps (s)")
    b.set_ylabel("\u03C9 (rad/s)")
    # Changement des couleurs de b
    change_subplot_color(b, "#3c3f41", "w")

    # Creation du subplot c qui represente lacceleration angulaire
    c = fig1.add_subplot(3, 1, 3)
    c.set_title("Acceleration p/r au temps")
    c.plot(t, a_w, label="a")
    c.legend()
    c.set_xlabel("Temps (s)")
    c.set_ylabel("Acceleration angulaire (rad/s²)")
    # Changement des couleurs de c
    change_subplot_color(c, "#3c3f41", "w")

    # On paque le plot dans un canevas dans wind
    bar1 = FigureCanvasTkAgg(fig1, wind)
    bar1.get_tk_widget().grid(row=3, column=0, pady=20, padx=20)


def diagramme_de_phase(wind, lsts_pst):

    x, v, a_w, y_1, y_2 = lsts_pst

    fig = Figure()
    fig.patch.set_facecolor("#3c3f41")
    a = fig.add_subplot(111)
    a.set_title("Diagramme de phase")
    a.plot(x, v)
    a.set_xlabel("theta (rad)")
    a.set_ylabel("\u03C9 (rad/s)")

    # Changement des couleurs
    change_subplot_color(a, "#3c3f41", "w")

    bar2 = FigureCanvasTkAgg(fig, wind)
    bar2.get_tk_widget().grid(row=3, column=2, padx=20)


# def graphiques_energie(wind, c_init, t, lsts_pst):
#     """
#     Affiche un graphique contenant une courbe l'energie potentielle, une de l'en. cinetique et une de l'en. totale
#
#     :param wind: fenetre dans laquelle les graphiques doivent s'afficher
#     :param c_init:
#     :param t: tableau des temps
#     :param lsts_pst: tuple contenant les listes x, v et a representant respectivement l'angle d'inclinaison, la
#                                                    vitesse angulaire et l'acceleration angulaire par rapport au temps
#
#     :return: -
#     """
#
#     _, _, k, _, m, _, _ = c_init
#     x, v, a_w, _,  _ = lsts_pst
#
#     en_tot = np.empty_like(t)
#     en_poussee = np.empty_like(t)
#     en_charge = np.empty_like(t)
#     for i in range(len(t)):
#         x = 0
#
#     fig2 = Figure()
#     a = fig2.add_subplot(111)
#     a.set_title("Energie p/r au temps")
#     a.plot(t, e_ressort, label="ressort")
#     a.plot(t, e_cin, label="cinétique")
#     a.plot(t, e_tot, label="total")
#     a.legend()
#     bar2 = FigureCanvasTkAgg(fig2, wind)
#     bar2.get_tk_widget().grid(row=3, column=2)


def graphique_var_charge(wind, info):
    g, h1, h2, l, m1, m2, m3_l, d, rho = info
    # TODO !!! m3[0]
    m3 = m3_l[0]

    theta = np.empty_like(d)

    for i in range(len(d)):

        info2 = (g, h1, h2, l, m1, m2, m3, d[i], rho)

        theta[i] = recherche_theta(info2)[0]

    submertion = np.full_like(d, theta_max(h1, enfoncement(rho, l, m1 + m2 + m3), l)[0])
    soulevement = np.full_like(d, theta_max(h1, enfoncement(rho, l, m1 + m2 + m3), l)[1])

    fig = Figure()
    fig.patch.set_facecolor("#3c3f41")
    a = fig.add_subplot(111)
    a.set_title("Angle de stabilite p/r a la distance")
    a.set_xlabel("Distance [m]")
    a.set_ylabel("Theta (rad)")
    a.plot(d, theta, label=f"m3 = {m3}kg")
    a.plot(d, submertion, "--", label="Submertion")
    a.plot(d, soulevement, "--", label="Soulevement")
    a.legend()

    # Changement des couleurs
    change_subplot_color(a, "#3c3f41", "w")

    bar2 = FigureCanvasTkAgg(fig, wind)
    bar2.get_tk_widget().pack()
