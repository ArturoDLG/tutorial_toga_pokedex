import toga
import requests
import threading
from const import *
from toga.style.pack import *

class PokeDex(toga.App):

    def __init__(self, title, id):
        """
        Inicializador de la ventana
        """

        # Aspectos de la ventana
        toga.App.__init__(self, title, id)
        self.title = title
        self.size = (WIDTH, HEIGHT)
        
        self.offset = 0

        self.response_name = ''
        self.response_description = ''
        self.response_sprite = ''

        
        # Aspectos de la tabla
        self.heading = ['Name']
        self.data = []

        # Llamada a los datos de la API
        
        self.create_elemets()
        self.load_async_data()
        self.validate_previous_command()

    def startup(self):
        """
        Personalizacion de la ventana
        """
        
        # ventana principal
        self.main_window = toga.MainWindow(title=self.title,
                                            size=self.size)
        # contenedor
        information_area = toga.Box(
            children=[self.image_view, self.pokemon_name, self.pokemon_description],
            style=Pack(direction=COLUMN)
        )
        
        # divisor de contenedor
        split = toga.SplitContainer()
        split.content = [self.table, information_area]
        
        self.main_window.content = split
        self.main_window.toolbar.add(self.previous_command, self.next_command)
        # self.commands.add(self.previous_command, self.next_command)
        self.main_window.show()

    def create_elemets(self):
        """
        Crear los elementos de la ventana
        """
        self.create_table()
        self.create_toolbar()
        self.create_image(PIDGEY_ICON)
        self.create_labels()

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
                                         tooltip='Next', icon=BULBASAUR_ICON)

    def create_previous_command(self):
        """
        Comando para navegar hacia atras
        """
        self.previous_command = toga.Command(self.previous, label='Previous', 
                                             tooltip='Previous', icon=METAPOD_ICON)

    def create_table(self):
        """
        Crear la tabla para visualizar los pokemones 
        """
        self.table = toga.Table(self.heading, data=self.data, on_select=self.select_element)

    def create_image(self, path, width=200, height=200):
        """
        Crear un ImageView para desplegar la imagen
        """
        image = toga.Image(path)
        style = Pack(width=width, height=height)
        self.image_view = toga.ImageView(image, style=style)

    def create_labels(self):
        self.pokemon_name = toga.Label('Name')
        self.pokemon_name.style.font_size = 20
        self.pokemon_name.style.padding_bottom = 10
        self.pokemon_description = toga.Label('Description')
    
    def load_async_data(self):
        """
        Cargar datos de forma asincrona
        """
        self.data.clear()
        self.table.data = self.data
        self.image_view.image = PIDGEY_ICON # None
        self.pokemon_name.text = 'Loading...'
        self.pokemon_description.text = ''
        thread = threading.Thread(target=self.load_data)
        thread.start()
        thread.join()
        self.table.data = self.data
        self.pokemon_name.text = 'Name'


    def load_async_pokemon(self, pokemon):
        """
        Obtener los datos de forma asincrona
        """
        thread = threading.Thread(target=self.load_pokemon, args=[pokemon])
        thread.start()
        thread.join()
        self.image_view.image = toga.Image(self.response_sprite)
        self.pokemon_name.text = self.response_name
        self.pokemon_description.text = self.response_description
        

    def load_pokemon(self, pokemon):
        """
        Obtener los datos de un Pokemon a traves
        de la API.
        """
        path = f'https://pokeapi.co/api/v2/pokemon/{pokemon}/'

        response = requests.get(path)
        if response:
            result =  response.json()
            self.response_name = result['forms'][0]['name']
            abilities = (ability['ability']['name'] 
                         for ability in result['abilities'])
            self.response_description = '\n'.join(abilities)
            self.response_sprite = result['sprites']['front_default']


    def load_data(self):
        """
        Cargar los datos de la PokeAPI
        """
        # Endpoint de la API
        path = f'https://pokeapi.co/api/v2/pokemon-form?offset={self.offset}&limit=20'

        # obtener datos de la API
        response =  requests.get(path)
        if response: 
            
            # Convertir la respuesta a ditc
            result = response.json()

            for pokemon in result['results']:
                name = pokemon['name']
                self.data.append(name) 

    # Callback
    def select_element(self, widget, row):
        """
        Callback para obtener la informacion de un determinado
        pokemon.
        """
        if row:
            self.load_async_pokemon(row.name)

    def next(self, widget):
        """
        """
        self.offset += 1
        self.load_async_data()
        self.handler_command(widget)

    def previous(self, widget):
        """
        Comando para obtener una pagina previa
        """
        self.offset -= 1
        self.handler_command(widget)

    def handler_command(self, widget):
        """
        Comando para obtener una pagina posterior
        """
        widget.enable = False
        self.load_async_data()
        widget.enabled = True
        self.validate_previous_command()

    def validate_previous_command(self):
        """
        Funcion para validar que offset no sea menor a 0
        inhabilitando previous_command.
        """
        self.previous_command.enabled = not (self.offset == 0)

if __name__ == "__main__":
    pokedex = PokeDex('PokeDex', 'com.example.Pokedex')
    pokedex.main_loop()