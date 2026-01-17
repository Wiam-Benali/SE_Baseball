import copy

import networkx as nx

from database.dao import DAO
from operator import itemgetter


class Model:
    def __init__(self):
        self.anni = None
        self.teams = None

        #grafo
        self.G = nx.Graph()
        self.salari = None

        #ricorsione
        self.sol_ottimale = None
        self.peso_ottimale = [0]



    def get_anni(self):
        self.anni = DAO.read_anni()

        return self.anni

    def get_teams(self,anno):
        self.teams = DAO.read_team(anno)
        num = len(self.teams)
        return self.teams,num

    def build_graph(self,anno):
        self.G.clear()

        self.G.add_nodes_from(self.teams.values())
        self.salari = DAO.read_salary_team(anno)

        coppie_distinte = []
        for team in self.teams:
            for team2 in self.teams:
                if sorted((team,team2)) not in coppie_distinte and team!=team2:
                    coppie_distinte.append(sorted((team,team2)))

        for coppia in coppie_distinte:
            salario = self.salari[coppia[0]] + self.salari[coppia[1]]
            self.G.add_edge(self.teams[coppia[0]],self.teams[coppia[1]],weight=salario)

    def get_dettagli(self,team):
        squadra_selezionata = self.teams[team]
        vicini = list(self.G[squadra_selezionata])

        risultato = []
        for vicino in vicini:
            risultato.append([vicino, self.G[squadra_selezionata][vicino]['weight']])
        risultato = sorted(risultato, key=itemgetter(1),reverse=True)
        return risultato


    def ricerca_max_percorso(self,cod_team):
        team = self.teams[cod_team]
        sol_parziale = [team]
        pesi_correnti = [0]
        self.ricorsione(sol_parziale,pesi_correnti)

        return self.sol_ottimale,self.peso_ottimale



    def ricorsione(self,sol_parziale,pesi_correnti):

        ultimo = sol_parziale[-1]
        ultimo_peso = pesi_correnti[-1]
        nodi_amissiibili = self.nodi_validi(ultimo,sol_parziale,ultimo_peso)

        if len(nodi_amissiibili)==0:
            if sum(pesi_correnti)>sum(self.peso_ottimale):
                self.peso_ottimale = copy.deepcopy(pesi_correnti)
                self.sol_ottimale = copy.deepcopy(sol_parziale)


        for nodo,peso in nodi_amissiibili:
            sol_parziale.append(nodo)
            pesi_correnti.append(peso)
            self.ricorsione(sol_parziale,pesi_correnti)
            sol_parziale.pop()
            pesi_correnti.pop()


    def nodi_validi(self,ultimo,sol_parziale,ultimo_peso):
        vicini = self.G[ultimo]
        pesi = []

        for vicino in vicini:
            pesi.append((vicino,self.G[ultimo][vicino]['weight']))

        pesi = sorted(pesi, key=itemgetter(1), reverse=True)
        validi = []

        if ultimo_peso==0:
            validi = pesi[:3]
        else:

            for nodo,peso in pesi:
                if peso<ultimo_peso and nodo not in sol_parziale:
                    validi.append((nodo,peso))

        return validi[:3]



