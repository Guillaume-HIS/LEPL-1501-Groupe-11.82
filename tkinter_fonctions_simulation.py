"""
    @author : Groupe 11.82
    @version : 15 novembre 2020

    Ce fichier contient les fonctions responsables de l'affichage sur la fenetre
"""


from tkinter import *
from PIL import ImageTk, Image
from fonctions_math_simulation import *


# Cree et ouvre une fenetre

wn = Tk()


def window_init(wn_name):
    """
    Donne un nom, une taille par defaut et minimum et une couleur de fond gets la fenetre

    :param wn_name: nom de la fenetre gets modifier

    :return: -
    """

    wn_name.title("Simulation")
    wn_name.geometry("1500x900")
    wn_name.minsize(1080, 720)
    wn_name.config(bg="#3c3f41")


def slide0():
    """
    Page de choix du type de simulation : - distance fixe et donc simulation de l'angle, vitesse et accel angulaire
                                          - distance variable, simulation de l'angle d'inclinaison en fonction
                                            de la charge

    :return: le type de simulation : 1 ou 2
    """

    def choice_all_static():
        nonlocal sim_type
        sim_type = 1
        var.set(1)
        return

    def choice_d_variable():
        nonlocal sim_type
        sim_type = 2
        var.set(1)
        return

    def on_quit():
        nonlocal sim_type
        sim_type = None
        var.set(1)
        return

    var = IntVar()
    sim_type = 0
    wn.protocol("WM_DELETE_WINDOW", on_quit)

    # Ajoute le frame
    frame0 = Frame(wn, bg="#3c3f41")
    label_title = Label(frame0, text="Choix du type de simulation", font=("Courrier", 25),
                        bg="#3c3f41", fg="white")
    label_title.pack(pady=75)

    # Ajout d'un subframe dans frame0 contenant une grille
    frame0_1 = Frame(frame0, bg="#3c3f41")
    frame0_1.grid_rowconfigure(3)
    frame0_1.grid_columnconfigure(3)

    # Cree le bouton correspondant gets la sim avec d fixe ainsi que son label et les paque dans frame0_1
    label_all_static = Label(frame0_1, text="Distance et charge fixe", font=("Courrier", 20),
                             bg="#3c3f41", fg="white")
    label_all_static.grid(row=0, column=0, padx=50)
    picture1 = ImageTk.PhotoImage(Image.open("image_enoncee_all_static.png").resize((400, 222), Image.ANTIALIAS))
    button_all_static = Button(frame0_1, image=picture1, bg="#99cccc", fg="black", command=choice_all_static)
    button_all_static.grid(row=1, column=0, padx=50)

    # Cree le bouton correspondant gets la sim avec d variable ainsi que son label et les paque dans frame0_1
    label_variable = Label(frame0_1, text="Distance variable et chage fixe", font=("Courrier", 20),
                           bg="#3c3f41", fg="white")
    label_variable.grid(row=0, column=2, padx=50)
    picture2 = ImageTk.PhotoImage(Image.open("image_enoncee_d_variable.png").resize((400, 222), Image.ANTIALIAS))
    button_variable = Button(frame0_1, image=picture2, bg="#99cccc", fg="black", command=choice_d_variable)
    button_variable.grid(row=1, column=2, padx=50)

    nothing = Label(frame0_1, bg="#3c3f41")
    nothing.grid(row=2, column=0, pady=10)

    # Ajout d'un subframe dans frame0 contenant une grille
    frame0_2 = Frame(frame0, bg="#3c3f41")
    frame0_2.grid_rowconfigure(2)
    frame0_2.grid_columnconfigure(1)

    frame0_1.pack()

    # Cree le logo de groupe affiche entre les deux boutons de sim
    picture_logo = ImageTk.PhotoImage(Image.open("logo2.png").resize((200, 200), Image.ANTIALIAS))
    logo = Label(frame0, image=picture_logo, bd=0)
    logo.pack(pady=25)

    frame0_2.pack()
    frame0.pack()

    button_all_static.wait_variable(var)

    frame0.destroy()

    return sim_type


def slide1(sim_type, dico_grue):
    """
    Premier "slide", premiere page que la fenetre va afficher apres le choix du type de simulation

    :return: le tuple input contenant les infos que l'utilisateur gets entre
    """

    def place_title():

        # Definit l'image et le texte gets afficher en fonction du type de simulation
        if sim_type == 1:
            img_name = "image_enoncee_all_static.png"
            txt = "Simulation avec distance et charge fixes"
        elif sim_type == 2:
            img_name = "image_enoncee_d_variable.png"
            txt = "Simulation avec distance variable et charge fixe"
        else:
            img_name = None
            txt = None

        # Ajoute texte
        label_title = Label(frame1, text=txt, font=("Courrier", 25),
                            bg="#3c3f41", fg="white")
        label_title.pack(pady=10)
        # Ajout image
        opened = Image.open(img_name)
        resized = opened.resize((500, 278), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized)
        panel1 = Label(frame1, image=img)
        panel1.img = img
        panel1.pack()

    def get_inputs(ntng=None):
        """ Recupere ce qui gets ete entre dans les entry box et met tout dans le tuple de fonction inputs et definit var

        :return: -
        """

        nonlocal inputs

        try:
            if sim_type == 1:
                tpl = float(entry_l.get()), float(entry_d.get()), None, float(entry_m1.get()), \
                      float(entry_m2.get()), float(entry_m3.get()), None, float(entry_h1.get()), float(entry_h2.get())
            else:
                tpl = float(entry_l.get()), float(entry_d1.get()), float(entry_d2.get()), float(entry_m1.get()), \
                      float(entry_m2.get()), float(entry_m3.get()), None, float(entry_h1.get()), float(entry_h2.get())
            frame1.forget()
            inputs = tpl
            var.set(1)
            return

        except ValueError:
            error_window()
            return

    def error_window():
        """ Affiche une fenetre d'erreur informant l'user de remplir tous le champs et de n'entrer que des nombres

        :return: -
        """

        def destroy_wn():
            """ Detruit la fenetre d'erreur

            :return: -
            """

            error.destroy()

        error = Tk()
        error.title("Error")
        error.geometry("400x125")
        error.minsize(400, 125)
        error.config(bg="white")
        txt = Label(error, text="Veuillez remplir tous les champs\net n'entrer que des nombres !",
                    font=("Courrier", 15), bg="white", fg="black")
        txt.pack()
        ok_button = Button(error, text="OK", font=("Courrier", 20),
                           bg="white", fg="black", command=destroy_wn)
        ok_button.pack(pady=15)
        error.mainloop()

    def go_back():
        frame1.forget()
        var.set(1)
        return

    def bind_enter():
        boxes = []

        if sim_type == 1:
            boxes = [entry_l, entry_d, entry_m1, entry_m2, entry_m3, entry_h1, entry_h2]
        elif sim_type == 2:
            boxes = [entry_l, entry_d1, entry_d2, entry_m1, entry_m2, entry_m3, entry_h1, entry_h2]

        for box in boxes:
            box.bind("<Return>", get_inputs)

        return

    def notre_grue():

        nonlocal our_crane
        our_crane = True

        # Remplissage entry box largeur
        entry_l.delete(0, END)
        entry_l.insert(0, str(dico_grue["largeur"]))

        # Remplissage entry box m1
        entry_m1.delete(0, END)
        entry_m1.insert(0, str(dico_grue["m1"]))

        # Remplissage entry box m2
        entry_m2.delete(0, END)
        entry_m2.insert(0, str(dico_grue["m2"]))

        # Remplissage entry box h1
        entry_h1.delete(0, END)
        entry_h1.insert(0, str(dico_grue["h1"]))

        # Remplissage entry box largeur
        entry_h2.delete(0, END)
        entry_h2.insert(0, str(dico_grue["h2"]))

    def on_quit():
        nonlocal inputs
        inputs = 1
        var.set(1)
        return

    # Cree deux variables locales
    var = IntVar()
    inputs = 0
    our_crane = False
    wn.protocol("WM_DELETE_WINDOW", on_quit)

    # Ajoute frame1
    frame1 = Frame(wn, bg="#3c3f41")

    # Ajoute texte et image d'enoncee en fonction du type de simulation

    place_title()

    # Cree un sub-frame dans frame 1 et y cree une grille de 8x3 dans laquelle les entry box et leurs titres seront
    frame1_1 = Frame(frame1, bg="#3c3f41", bd=0, highlightthickness=0)
    frame1_1.grid_rowconfigure(10)
    frame1_1.grid_columnconfigure(3)

    # Entry box de L et son titre
    label_l = Label(frame1_1, text="Valeur de L [m]:", font=("Courrier", 10),
                    bg="#3c3f41", fg="white")
    label_l.grid(row=0, column=0, padx=25)
    entry_l = Entry(frame1_1)
    entry_l.grid(row=1, column=0, padx=25)

    # Entry boxes de d1 et d2 et leurs titres pour sim avec d variable
    if sim_type == 2:
        # d1 ------------------
        label_d1 = Label(frame1_1, text="Valeur de d1 [m]:", font=("Courrier", 10),
                         bg="#3c3f41", fg="white")
        label_d1.grid(row=3, column=0, padx=25)
        entry_d1 = Entry(frame1_1)
        entry_d1.grid(row=4, column=0, padx=25)
        # d2 -------------------
        label_d2 = Label(frame1_1, text="Valeur de d2 [m]:", font=("Courrier", 10),
                         bg="#3c3f41", fg="white")
        label_d2.grid(row=6, column=0, padx=25)
        entry_d2 = Entry(frame1_1)
        entry_d2.grid(row=7, column=0, padx=25)

    # Entry box de D et son titre pour sims avec d fixe
    else:
        label_d = Label(frame1_1, text="Valeur de d [m]:", font=("Courrier", 10),
                        bg="#3c3f41", fg="white")
        label_d.grid(row=3, column=0, padx=25)
        entry_d = Entry(frame1_1)
        entry_d.grid(row=4, column=0, padx=25)

    # Nothing est un label vide qui permet d'occuper les positions 2;1 et 5;1 afin d'y creer un espace
    nothing = Label(frame1_1, bg="#3c3f41")
    nothing2 = Label(frame1_1, bg="#3c3f41")
    nothing.grid(row=2, column=1, padx=25)
    nothing2.grid(row=5, column=1, padx=25)

    # Entry box de m1 et son titre
    label_m1 = Label(frame1_1, text="Valeur de m1 [kg]:", font=("Courrier", 10),
                     bg="#3c3f41", fg="white")
    label_m1.grid(row=0, column=1, padx=25)
    entry_m1 = Entry(frame1_1)
    entry_m1.grid(row=1, column=1, padx=25)

    # Entry box de m2 et son titre
    label_m2 = Label(frame1_1, text="Valeur de m2 [kg]:", font=("Courrier", 10),
                     bg="#3c3f41", fg="white")
    label_m2.grid(row=3, column=1, padx=25)
    entry_m2 = Entry(frame1_1)
    entry_m2.grid(row=4, column=1, padx=25)

    # Entry box de m3 et son titre
    label_m3 = Label(frame1_1, text="Valeur de m3 [kg]:", font=("Courrier", 10),
                     bg="#3c3f41", fg="white")
    label_m3.grid(row=6, column=1, padx=25)
    entry_m3 = Entry(frame1_1)
    entry_m3.grid(row=7, column=1, padx=25)

    # Entry box de h1 et son titre
    label_h1 = Label(frame1_1, text="Valeur de h1 [m]:", font=("Courrier", 10),
                     bg="#3c3f41", fg="white")
    label_h1.grid(row=0, column=2, padx=25)
    entry_h1 = Entry(frame1_1)
    entry_h1.grid(row=1, column=2, padx=25)

    # Entry box de h2 et son titre
    label_h2 = Label(frame1_1, text="Valeur de h2 [m]:", font=("Courrier", 10),
                     bg="#3c3f41", fg="white")
    label_h2.grid(row=3, column=2, padx=25)
    entry_h2 = Entry(frame1_1)
    entry_h2.grid(row=4, column=2, padx=25)

    bind_enter()

    # On paque frame1_1 dans frame1
    frame1_1.pack(pady=50, padx=10)

    # Cree un subfame dans frame1 et y cree une grille
    frame1_2 = Frame(frame1, bg="#3c3f41", bd=0, highlightthickness=0)
    frame1_2.grid_rowconfigure(1)
    frame1_2.grid_columnconfigure(3)

    # Cree le bouton valider et le pacque dans frame1_2
    button_validate = Button(frame1_2, text="Valider", font=("Courrier", 25),
                             bg="#99cccc", fg="black", command=get_inputs)
    button_validate.grid(row=0, column=1, padx=50)

    # Cree le bouton de retour en arriere
    button_back = Button(frame1_2, text="BACK", font=("Courrier", 15),
                         bg="#99cccc", fg="black", command=go_back)
    button_back.grid(row=0, column=0)

    # Cree le bouton qui replis les entry boxes par les valeurs de la grue
    button_fill = Button(frame1_2, text="Notre Grue", font=("Courrier", 15),
                         bg="#99cccc", fg="black", command=notre_grue)
    button_fill.grid(row=0, column=2)

    # Pacque frame1_2 dans frame1
    frame1_2.pack()

    # Paque frame1 dans la fenetre wn
    frame1.pack()

    # Var est une wait_variable, tant qu'elle n'est pas set, le programme attend, ici, elle est set dans get_inputs
    button_validate.wait_variable(var)

    # Renvoie le tuple inputs contenant toutes les entrees des entry box
    return inputs, our_crane


def slide_d_static(infos, c_init, t, lsts_pst):
    """ Deuxieme "slide", deuxieme page que la fenetre va afficher, contient la valeur de l'angle en degres et radians
        et les graphes correspondant aux fonctions graphiques et graphiques_energie

    :param infos: tuples des infos du systeme (voir main_simulation pour son contenu)
    :param c_init:
    :param t: tableau des temps
    :param lsts_pst: tuple contenant les listes x, v et gets representant respectivement l'angle d'inclinaison, la vitesse
                       angulaire et l'acceleration angulaire par rapport au temps

    :return: Un boleen : True si le bouton HOME gets ete presse, False sinon
    """

    def go_home():
        """ Fonction appelee quand la bouton HOME est presse, definit keep_going gets True et set wait_var

        :return: None
        """

        nonlocal keep_going
        keep_going = True
        wait_var.set(1)
        return

    def on_quit():
        nonlocal keep_going
        keep_going = False
        wait_var.set(1)
        return

    keep_going = False
    wait_var = IntVar()
    wn.protocol("WM_DELETE_WINDOW", on_quit)

    # Création frame
    frame2 = Frame(wn, bg="#3c3f41")

    # Creation 1er subframe avec grille
    frame2_1 = Frame(frame2, bg="#3c3f41", bd=0, highlightthickness=0)
    frame2_1.grid_rowconfigure(4)
    frame2_1.grid_columnconfigure(3)

    # Creation labels et positionnement de ceux-ci sur la grille de frame2_1
    tlt_rad = Label(frame2_1, text="Angle d'équilibre en radians :", font=("Courrier", 15),
                    bg="#3c3f41", fg="white")
    tlt_deg = Label(frame2_1, text="Angle d'équilibre en degrés :", font=("Courrier", 15),
                    bg="#3c3f41", fg="white")
    ang_rad = Label(frame2_1, text=f'{recherche_theta(infos)[0]}', font=("Courrier", 20),
                    bg="#3c3f41", fg="white")
    ang_deg = Label(frame2_1, text=f'{recherche_theta(infos)[1]}', font=("Courrier", 20),
                    bg="#3c3f41", fg="white")
    tlt_rad.grid(row=0, column=0, padx=50)
    ang_rad.grid(row=1, column=0, padx=50)
    tlt_deg.grid(row=0, column=2, padx=50)
    ang_deg.grid(row=1, column=2, padx=50)

    # Appel des fonctions qui affichent les graphiques
    graphiques(frame2_1, t, lsts_pst)
    diagramme_de_phase(frame2_1, lsts_pst)

    home_button = Button(frame2, text="HOME", font=("Courrier", 25),
                         bg="#1f77b4", fg="black", command=go_home)
    home_button.pack(side="bottom", pady=25)

    # On paque frame2_1 et frame2 respectivement dans frame2 et wn
    frame2_1.pack()
    frame2.pack()

    # Tant que wait_var n'est pas set, le programme est en sleep
    home_button.wait_variable(wait_var)

    # On detruit le frame2
    frame2.forget()

    return keep_going


def slide_d_variable(infos, t):
    """ Deuxieme "slide", deuxieme page que la fenetre va afficher, contient la valeur de l'angle en degres et radians
            et les graphes correspondant aux fonctions graphiques et graphiques_energie

        :param infos: tuples des infos du systeme (voir main_simulation pour son contenu)
        :param t: tableau des temps

        :return: Un boleen : True si le bouton HOME gets ete presse, False sinon
    """

    def go_home():
        """ Fonction appelee quand la bouton HOME est presse, definit keep_going gets True et set wait_var

        :return: None
        """

        nonlocal keep_going
        keep_going = True
        wait_var.set(1)
        return

    def on_quit():
        nonlocal keep_going
        keep_going = False
        wait_var.set(1)
        return

    keep_going = False
    wait_var = IntVar()
    wn.protocol("WM_DELETE_WINDOW", on_quit)

    # Création frame
    frame2 = Frame(wn, bg="#3c3f41")

    graphique_var_charge(frame2, infos)

    home_button = Button(frame2, text="HOME", font=("Courrier", 25),
                         bg="#99cccc", fg="black", command=go_home)
    home_button.pack(pady=50)

    frame2.pack()

    home_button.wait_variable(wait_var)

    frame2.forget()

    return keep_going
