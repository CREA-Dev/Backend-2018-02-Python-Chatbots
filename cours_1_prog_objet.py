
# Definition des variables

class Artist:

    first_name = "Test"
    last_name = "Famille"
    talent = 0
    styles = None
    albums = None
    label = None

    def __init__(self, initial_first_name, initial_last_name):
        self.first_name = initial_first_name
        self.last_name = initial_last_name
        self.albums = []
        self.styles = []

    def crie_ton_nom(self):
        return self.last_name.upper()

    def add_album(self, title):
        self.albums.append(title)

    def signed_new_contract(self, new_label):
        self.label = new_label


class Label:

    name = None
    creation_year = 0

    def __init__(self, name, year):
        self.name = name
        self.creation_year = year




# Debut du programme

nouvel_artiste = Artist("Michel", "Dupont")

famous_label = Label("Famous", 2018)


nouvel_artiste.signed_new_contract(famous_label)

print(nouvel_artiste.label.name)

