import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        try:
            anno = int(self._view.dd_anno.value)
            self._model.build_graph(anno)

        except ValueError:
            self._view.show_alert(f"Inserire un'anno prima di proseguire")

    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        team = self._view.dd_squadra.value
        if team is not None:
           dettagli = self._model.get_dettagli(team)
           for (vicino,peso) in dettagli:
               self._view.txt_risultato.controls.append(ft.Text(f"{vicino.team_code}({vicino.name}) - peso : {peso}"))
        else:
            self._view.show_alert('Selezionare una squadra')

        self._view.update()

    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        team = self._view.dd_squadra.value
        if team is not None:
            sol,pesi = self._model.ricerca_max_percorso(team)
            for i in range(len(sol)-1):
                self._view.txt_risultato.controls.append(ft.Text(f"{sol[i].team_code}({sol[i].name})---> {sol[i+1].team_code}({sol[i+1].name})- peso : {pesi[i+1]}"))
            self._view.txt_risultato.controls.append(ft.Text(f'Peso totale : {sum(pesi)}'))
        else:
            self._view.show_alert('Selezionare una squadra')

        self._view.update()


    """ Altri possibili metodi per gestire di dd_anno """""
    def populate_dd(self):

        anni = self._model.get_anni()
        for anno in anni:
            self._view.dd_anno.options.append(ft.dropdown.Option(anno))
        self._view.update()

    def handle_teams(self,e):

        try:

            anno = int(self._view.dd_anno.value)
            teams,num = self._model.get_teams(anno)
            self._view.txt_out_squadre.controls.clear()
            self._view.txt_out_squadre.controls.append(ft.Text(f'Numero squadre: {num}'))
            for cod in teams:
                self._view.txt_out_squadre.controls.append(ft.Text(f'{cod} ({teams[cod].name})'))
                self._view.dd_squadra.options.append(ft.dropdown.Option(content=ft.Text( f'{cod} ({teams[cod].name})') ,key = cod))

        except ValueError:
            self._view.show_alert('Deve essere selezionato un anno')

        self._view.update()