from os import chdir
from random import randint
import sys


def decoupe_tab(li):
    return li.strip().split("\t")


def import_distrib_ressources(path):
    f_in = open( path, 'r')
    tab = []
    li = f_in.readline()
    while ( li != "" ) :
        a = decoupe_tab(li)
        i = 0
        while i < int(a[1]):
            tab.append(a[0])
            i += 1
        li = f_in.readline()
    f_in.close
    return tab


def init_coffre(path):
    f_in = open( path, 'r')
    chest = {}
    li = f_in.readline()
    while ( li != "" ) :
        a = decoupe_tab(li)
        chest[a[0]]= 0
        li = f_in.readline()
    f_in.close
    return chest


def store_score(path, name, score):
    f_out = open( path, 'a')
    li = name + "\t" + str(score) + "\n"
    f_out.write(li)
    f_out.close


def fixe_longueur( chaine, longueur ):
    return chaine.rjust(longueur, " ")


def liste_items(coffre ):
    return list(coffre.keys())


def ouvre_coffre( coffre ):
    items = liste_items(coffre)
    for i in range(0, len(items) ):
        print(fixe_longueur(items[i], 15), coffre[items[i]])


def ajoute(coffre, item):
    coffre[item] += 1


def ajoute_plusieurs( coffre, panier ) :
    for i in range(0, len(panier)):
        ajoute(coffre, panier[i])


def est_present( coffre, item):
    if int(coffre[item]) > 0:
        return True
    else:
        return False


def est_assez(coffre, item, count):
	if int(coffre[item]) >= int(count):
		return True
	else:
		return False


def sont_presents( coffre, liste_item):
	for i in range(0, len(liste_item)):
		if not est_present( coffre, liste_item[i]):
			return False
	return True


def sont_assez(coffre, liste_item, counts):
	for i in range(0, len(liste_item)):
		if not est_assez( coffre, liste_item[i], counts[i]):
			return False
	return True


def retire( coffre, item):
    if est_present(coffre, item):
        coffre[item] -= 1
        return True
    else:
        return False


def retire_plusieurs( coffre, liste_item):
    if sont_presents(coffre, liste_item):
        for i in range(0, len(liste_item)):
            coffre[liste_item[i]] -= 1
        return True
    else:
        return False


def glaner(ressources, quantite):
    objets_glanes = []
    for i in range(0, quantite):
        objets_glanes.append(ressources[randint(0,len(ressources) -1)])
    return objets_glanes


def import_regles_craft(path):
	f_in = open( path, 'r')
	regles_craft = {}
	li = f_in.readline();
	lj = f_in.readline()
	while (li != "" or lj != ""):
		if li[0] == "#":
			li = lj
			lj = f_in.readline()
		if  lj != "" and lj[0] == "#":
			li = f_in.readline()
			lj = f_in.readline()
		a = decoupe_tab(li)
		ingredients = {"count" : a[1]}
		i = 2
		while i < len(a) -1:
			ingredients[a[i]] = a[i+1]
			i += 2
		regles_craft[a[0]] = ingredients
		li = lj
		lj = f_in.readline()
	f_in.close
	return regles_craft


def craft_possible(coffre, regles_craft, item) :
	liste_ingredients = liste_items(regles_craft[item])
	tmp = []
	for i in range(0, len(liste_ingredients)):
		if liste_ingredients[i] != "count":
			tmp.append(liste_ingredients[i])
	liste_ingredients = tmp
	counts = []
	for i in range(0, len(liste_ingredients)):
		shortcut = regles_craft[item]
		counts.append(shortcut[liste_ingredients[i]])
	if sont_assez(coffre, liste_ingredients, counts):
		return True
	else:
		return False


def craft(coffre, regles_craft, item, outils):
	if craft_possible(coffre, regles_craft, item):
		liste_ingredients = liste_items(regles_craft[item])
		tmp = []
		for i in range(0, len(liste_ingredients)):
			if liste_ingredients[i] != "count":
				tmp.append(liste_ingredients[i])
		liste_ingredients = tmp
		items_to_remove = []
		shortcut = regles_craft[item]
		for i in range(0, len(liste_ingredients)):
			if not liste_ingredients[i] in outils:
				items_to_remove += int(shortcut[liste_ingredients[i]]) * [liste_ingredients[i]]
		retire_plusieurs(coffre, items_to_remove)
		ajoute_plusieurs(coffre, int(shortcut["count"]) * [item])
		print("Vous avez craft l'item \"" + item + "\" en " + shortcut["count"] + " exemplaires.")
		return True
	else:
		return False


def manger(coffre, item, PdV, comestibles, name):
    liste_comestibles = liste_items(comestibles)
    for i in range(0, len(comestibles)):
        if item == liste_comestibles[i]:
            if est_present(coffre, item):
                print(name + " mange l'item \"" + item + "\" et récupère " + str(comestibles[item]) + " points de vie.")
                retire(coffre, item)
                PdV += comestibles[item]
                return PdV
            else:
                print("Erreur : Cet item n'est pas dans le coffre")
    print("Erreur : Cet item n'est pas comestible")
    return PdV


def maj_PdV(coffre, pdv, protections) :
    damage = 50
    liste_protections = liste_items(protections)
    for i in range(0, len(protections)):
        if coffre[liste_protections[i]] > 0:
            damage -= protections[liste_protections[i]]
    return pdv - damage


def est_dans( chaine, liste_de_chaine ):
    for i in range(0, len(liste_de_chaine)):
        if liste_de_chaine[i] == chaine:
            return True
    return False


def saisie_controlee( message, admissible) :
    n = None
    message += " "
    while n == None or not est_dans(n, admissible):
        n = input(message)
    return n


def choix_item(coffre) :
    return saisie_controlee("Choisissez un item du coffre", liste_items(coffre))


def crafts_possibles(coffre, regles_craft):
    a = liste_items(regles_craft)
    tmp = []
    for i in range(0, len(a)):
        if craft_possible(coffre, regles_craft, a[i]):
            tmp.append(a[i])
    return tmp



def manger_possibles(coffre, comestibles):
    a = liste_items(comestibles)
    tmp = []
    for i in range(0, len(a)):
        if est_present(coffre, a[i]):
            tmp.append(a[i])
    return tmp


def glaner_global(coffre, ressources, name):
	a = glaner(ressources, randint(0, 5))
	if len(a) > 0:
		ajoute_plusieurs(coffre, a)
		if len(a) == 1:
			print(name, "a glané l'élément suivant :", a[0])
		else:
			i = 0
			c = name + " a glané les éléments suivants : "
			while i < len(a) -1:
				c += a[i] + ", "
				i += 1
			c += a[i]
			print(c)
	else:
		print(name + " n'a rien trouvé !")

def craft_global(coffre, regles_craft, IA, outils, protections):
	liste_crafts = crafts_possibles(coffre, regles_craft)
	if liste_crafts == []:
		print("Vous ne pouvez rien craft.")
	while liste_crafts != []:
		if len(liste_crafts) == 1:
			print("Vous pouvez craft l'élément suivant :")
		else:
			print("Vous pouvez craft les éléments suivants :")
		for i in range(0, len(liste_crafts)):
			print("\t" + liste_crafts[i])
		if IA:
			item_to_craft = ""
			for i in range(0, len(protections)):
				protection = list(protections.keys())[i]
				if coffre[protection] == 0 and protection in liste_crafts:
					item_to_craft = protection
			for i in ['corde', 'clou']:
				if i in liste_crafts and coffre[i] < 15:
					item_to_craft = i
			for i in ['tissu']:
				if i in liste_crafts and coffre[i] < 5:
					item_to_craft = i
			for i in ['ble', 'coton', 'pain', 'tomate']:
				if i in liste_crafts:
					item_to_craft = i
			for i in range(0, len(outils)):
				outil = outils[i]
				if coffre[outil] == 0 and outil in liste_crafts:
					item_to_craft = outil
			if item_to_craft == "":
				item_to_craft = 'pass'
		else:
			liste_crafts.append("pass")
			item_to_craft = saisie_controlee("Veuillez saisir le nom de l'item que vous souhaitez craft ou saisir 'pass' pour ne rien craft :", liste_crafts)
		if item_to_craft == "pass" or item_to_craft == "'pass'":
			liste_crafts = []
		if liste_crafts != []:
			craft(coffre, regles_craft, item_to_craft, outils)
			liste_crafts = crafts_possibles(coffre, regles_craft)


def food_global(coffre, comestibles, PdV, name, IA):
	liste_nourriture = manger_possibles(coffre, comestibles)
	if liste_nourriture == []:
		print(name + " n'a rien à manger")
	while liste_nourriture != []:
		if len(liste_nourriture) == 1:
			print(name + " peut manger l'élément suivant :")
		else:
			print(name + " peut manger les éléments suivants :")
		for i in range(0, len(liste_nourriture)):
			print("\t" + liste_nourriture[i])
		if IA:
			if 'pain' in liste_nourriture:
				item_to_eat = 'pain'
			elif 'tomate' in liste_nourriture:
				item_to_eat = 'tomate'
			else:
				item_to_eat = 'pass'
		else:
			liste_nourriture.append("pass")
			item_to_eat = saisie_controlee("Veuillez saisir le nom de l'item que vous souhaitez faire manger à " + name + " ou saisir 'pass' pour ne rien lui donner :", liste_nourriture)
		if item_to_eat == "pass" or item_to_eat == "'pass'":
			liste_nourriture = []
		if liste_nourriture != []:
			PdV = manger(coffre, item_to_eat, PdV, comestibles, name)
			liste_nourriture = manger_possibles(coffre, comestibles)
	return PdV


def partie(ressources_path = "data/ressources", regles_craft_path = "data/regles_craft_plus", PdV = 1500):
	maxPdv = PdV
	IA = saisie_controlee("Voulez-vous faire jouer une IA ? Saisissez oui ou non :", ["oui", "non"])
	if IA == "oui":
		IA = True
	else:
		IA = False
	ressources = import_distrib_ressources(ressources_path)
	coffre = init_coffre(ressources_path)
	regles_craft = import_regles_craft(regles_craft_path)
	comestibles = {"pain" : 10, "tomate" : 5, "ble" : 1}
	outils = ["marteau", "metier_a_tisser", "beche", "aiguille", "panier"]
	protections = {"vetement" : 5, "lit" : 7, "hutte" : 15}
	if IA:
		name = "Cobaye"
	else:
		name = input("Veuillez renseigner le nom du personnage : ")
		print("\nBut du jeu :\nVous devez garder en vie " + name + ". À chaque tour, " + name + " va perdre des points de vie.\nVous pouvez craft des éléments pour protéger et nourrir " + name + ".\n")
	tours = 0
	while PdV > 0:
		glaner_global(coffre, ressources, name)
		craft_global(coffre, regles_craft, IA, outils, protections)
		PdV = food_global(coffre, comestibles, PdV, name, IA)
		PdV = maj_PdV(coffre, PdV, protections)
		tours += 1
		if PdV > 0:
			print("Vie de " + name +" : [" + str(PdV) + "/" + str(maxPdv) + "]")
			if not IA:
				pause = saisie_controlee("\nPressez ENTREE pour continuer ou saisissez 'coffre' pour afficher son contenu\nou'stop' pour fermer le jeu (" + name + " ne sera plus de ce monde).", ["", "stop", "coffre", "crafts"])
				while pause != "" and PdV > 0:
					if pause == "stop":
						PdV = 0
					if pause == "coffre":
						ouvre_coffre(coffre)
					if pause == "crafts":
						ouvre_coffre(regles_craft)
					pause = saisie_controlee("\nPressez ENTREE pour continuer ou saisissez 'coffre' pour afficher son contenu\nou'stop' pour fermer le jeu (" + name + " ne sera plus de ce monde).", ["", "stop", "coffre", "crafts"])
		else:
			print("GAME OVER : " + name + " est mort")
			ouvre_coffre(coffre)
		print("\n\n")
	store_score("data/scores", name, tours)



for i in range(0, 15):
	partie()
