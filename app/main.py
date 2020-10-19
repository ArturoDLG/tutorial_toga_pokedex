import toga
import requests
import threading
from const import *

class PokeDex(toga.App):

    def __init__(self, title, id):
        """
        Inicializador de la ventana
        """

        # Aspectos de la ventana
        toga.App.__init__(self, title, id)
        self.title = title
        self.size = (WIDTH, HEIGHT)
        
        # Aspectos de la tabla
        self.heading = ['Name']
        self.data = []

        # Llamada a los datos de la API
        self.create_elemets()
        self.load_async_data()

    def startup(self):
        """
        Personalizacion de la ventana
        """
        
        # ventana principal
        self.main_window = toga.MainWindow(title=self.title,
                                            size=self.size)
        # contenedor
        box = toga.Box()
        
        # divisor de contenedor
        split = toga.SplitContainer()
        split.content = [self.table, box]

        self.main_window.content = split
        self.main_window.toolbar.add(self.previous_command, self.next_command)
        self.main_window.show()

    def create_elemets(self):
        """
        Crear los elementos de la ventana
        """
        self.create_table()
        self.create_toolbar()

    def create_toolbar(self):
        """
        Crear barra de herramientas
        """
        self.create_previous_command()
        self.create_next_command()

    def create_next_command(self):
        """
        Comando para navegar hacia adelante
        """
        self.next_command = toga.Command(self.next, label='Next', 
                                         tooltip='Next', icon=str(BULBASAUR_ICON))

    def create_previous_command(self):
        """
        Comando para navegar hacia atras
        """
        self.previous_command = toga.Command(self.previous, label='Previous', 
                                             tooltip='Previous', icon=str(METAPOD_ICON))

    def create_table(self):
        """
        Crear la tabla para visualizar los pokemones 
        """
        self.table = toga.Table(self.heading, data=self.data, on_select=self.select_element)
    
    def load_async_data(self):
        """
        Cargar datos de forma asincrona
        """
        thread = threading.Thread(target=self.load_data)
        thread.start()

    def load_data(self):
        """
        Cargar los datos de la PokeAPI
        """

        # Endpoint de la API
        path = 'https://pokeapi.co/api/v2/pokemon-form?offset=0&limit=20'

        # obtener datos de la API
        if response:= requests.get(path):
            
            # Convertir la respuesta a ditc
            result = response.json()

            for pokemon in result['results']:
                name = pokemon['name']
                self.data.append(name) 

        self.table.data = self.data

    # Callback

    def select_element(self, widget, row):
        """
        Callback ... 
        """
        if row:
            print(row.name)

    def next(self, widget):
        print("Next")

    def previous(self, widget):
        print("Previous")

if __name__ == "__main__":
    pokedex = PokeDex('PokeDex', 'com.example.Pokedex')
    pokedex.main_loop()