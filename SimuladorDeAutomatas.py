import tkinter as tk
from tkinter import messagebox
import math

# Definición de la clase AFD
class AFD:
    def __init__(self): # Constructor de la clase AFD 
        self.estado_inicial = None # Inicializa el estado inicial en None 
        self.estados_finales = set() # Inicializa el conjunto de estados finales como un conjunto vacío 
        self.transiciones = {} # Inicializa el diccionario de transiciones como un diccionario vacío 
        self.todos_los_estados = set() # Inicializa el conjunto de todos los estados como un conjunto vacío 

    def configurar_estado_inicial(self, estado): # Método para configurar el estado inicial 
        if estado in self.todos_los_estados: # Verifica que el estado ingresado esté en el conjunto de todos los estados 
            self.estado_inicial = estado # Asigna el estado ingresado como estado inicial 
        else:
            raise ValueError("El estado inicial debe ser uno de los estados definidos en las transiciones.")

    def agregar_transicion(self, estado_origen, simbolo, estado_destino): # Método para agregar una transición 
        if estado_origen not in self.transiciones: # Verifica si el estado origen no está en el diccionario de transiciones 
            self.transiciones[estado_origen] = {} # Crea un diccionario vacío para el estado origen 
        elif simbolo in self.transiciones[estado_origen]: # Verifica si ya existe una transición con el mismo símbolo 
            raise ValueError(f"Transición no determinista detectada: desde {estado_origen} ya existe una transición con el símbolo {simbolo}.") # Muestra un mensaje de error si ya existe una transición con el mismo símbolo 
        self.transiciones[estado_origen][simbolo] = estado_destino # Asigna el estado destino al estado origen con el símbolo correspondiente 
        self.todos_los_estados.update([estado_origen, estado_destino]) # Actualiza el conjunto de todos los estados con los estados involucrados en la transición 

    
    def eliminar_transicion(self, estado_origen, simbolo): # Método para eliminar una transición 
        if estado_origen in self.transiciones and simbolo in self.transiciones[estado_origen]: # Verifica si el estado origen y el símbolo existen en el diccionario de transiciones 
            del self.transiciones[estado_origen][simbolo] # Elimina la transición del diccionario de transiciones 
            if not self.transiciones[estado_origen]: # Verifica si el estado origen no tiene más transiciones 
                del self.transiciones[estado_origen] # Elimina el estado origen del diccionario de transiciones 
    
    def eliminar_estado_si_es_huerfano(self, estado):
        # Un estado huerfano es aquel que no tiene transiciones entrantes ni salientes
        if estado not in self.transiciones and all(estado != destino for trans in self.transiciones.values() for destino in trans.values()): # Verifica si el estado no está en el diccionario de transiciones y si no es un estado destino en ninguna transición 
            self.todos_los_estados.discard(estado) # Elimina el estado del conjunto de todos los estados 
            self.estados_finales.discard(estado) # Elimina el estado del conjunto de estados finales 
            if self.estado_inicial == estado: # Verifica si el estado es el estado inicial 
                self.estado_inicial = None # Asigna None al estado inicial 
        
    def agregar_estado_final(self, estado): # Método para agregar un estado final 
        if estado in self.todos_los_estados: # Verifica si el estado está en el conjunto de todos los estados 
            self.estados_finales.add(estado) # Agrega el estado al conjunto de estados finales 
        else:
            raise ValueError("Los estados finales deben ser uno de los estados definidos en las transiciones.")
        
    def aceptar(self, cadena): # Método para verificar si una cadena es aceptada por el AFD 
        estado_actual = self.estado_inicial # Inicializa el estado actual con el estado inicial 
        for simbolo in cadena: # Itera sobre cada símbolo de la cadena 
            estado_actual = self.transiciones.get(estado_actual, {}).get(simbolo) # Obtiene el estado destino de la transición actual 
            if estado_actual is None: # Verifica si el estado actual es None 
                return False # Retorna False si no hay transición para el símbolo actual
        return estado_actual in self.estados_finales # Retorna True si el estado actual es un estado final, False en caso contrario 
    
    def obtener_datos_visuales(self):
        # Esta función retorna una estructura de datos con la información necesaria para dibujar el AFD
        return {
            'estados': self.todos_los_estados,
            'transiciones': self.transiciones,
            'estado_inicial': self.estado_inicial, 
            'estados_finales': self.estados_finales
        }

def agregar_transicion(): # Función para agregar una transición 
    estado_origen = entry_estado_origen.get() # Obtiene el estado origen ingresado en el campo de entrada 
    simbolo = entry_simbolo.get() # Obtiene el símbolo ingresado en el campo de entrada 
    estado_destino = entry_estado_destino.get() # Obtiene el estado destino ingresado en el campo de entrada 
    if estado_origen and simbolo and estado_destino: # Verifica si los campos de entrada no están vacíos 
        try: # Intenta agregar la transición 
            afd.agregar_transicion(estado_origen, simbolo, estado_destino) # Agrega la transición al AFD 
            listbox_transiciones.insert(tk.END, f"  {estado_origen} -- {simbolo} --> {estado_destino}") # Inserta la transición en la lista de transiciones 
            entry_estado_origen.delete(0, tk.END) # Limpia el campo de entrada del estado origen 
            entry_simbolo.delete(0, tk.END) # Limpia el campo de entrada del símbolo 
            entry_estado_destino.delete(0, tk.END) # Limpia el campo de entrada del estado destino 
        except ValueError as ve: 
            messagebox.showerror("Error de transición", str(ve)) # Muestra un mensaje de error si la transición no se puede agregar 
    else:
        messagebox.showwarning("Advertencia", "Todos los campos deben estar completos.") # Muestra un mensaje de advertencia si no se completan todos los campos
    actualizar_visualizacion() # Actualiza la visualización del AFD 

def eliminar_transicion(): # Función para eliminar una transición
    seleccion = listbox_transiciones.curselection() # Obtiene la selección actual en la lista de transiciones
    if seleccion: # Verifica si hay una selección 
        indice = seleccion[0] # Obtiene el índice de la selección 
        contenido = listbox_transiciones.get(indice) # Obtiene el contenido de la selección 
        estado_origen, resto = contenido.strip().split(' -- ') # Divide el contenido en el estado origen y el resto de la transición
        simbolo, estado_destino = resto.split(' --> ') # Divide el resto de la transición en el símbolo y el estado destino 
        simbolo = simbolo.strip() # Elimina los espacios en blanco del símbolo
        print("eliminando transicion de ", estado_origen, "con simbolo ", simbolo, "y destino ", estado_destino)
        afd.eliminar_transicion(estado_origen, simbolo) # Elimina la transición del AFD 
        afd.eliminar_estado_si_es_huerfano(estado_origen) # Elimina el estado origen si es un estado huérfano 
        afd.eliminar_estado_si_es_huerfano(estado_destino) # Elimina el estado destino si es un estado huérfano 
        listbox_transiciones.delete(indice) # Elimina la transición de la lista de transiciones
        print("Estado del AFD después de eliminar:")
        print("Transiciones:", afd.transiciones)
        print("Estados:", afd.todos_los_estados)
        print("Estados finales:", afd.estados_finales)
        actualizar_visualizacion() # Actualiza la visualización del AFD 
    else:
        messagebox.showwarning("Advertencia", "Seleccione una transición para eliminar.")


def configurar_estados(): # Función para configurar los estados iniciales y finales
    estado_inicial = entry_estado_inicial.get() # Obtiene el estado inicial ingresado en el campo de entrada 
    estados_finales = entry_estados_finales.get().split(',') # Obtiene los estados finales ingresados en el campo de entrada y los divide por comas 
    if not estado_inicial or not entry_estados_finales.get().strip(): # Verifica si el estado inicial o los estados finales no están ingresados
        messagebox.showwarning("Advertencia", "Debe ingresar tanto el estado inicial como al menos un estado final.") # Muestra un mensaje de advertencia si no se ingresan los estados necesarios
        return

    try:
        afd.configurar_estado_inicial(estado_inicial)
        afd.estados_finales.clear()  # Limpiar estados finales antes de agregar nuevos
        for estado_final in estados_finales: # Agregar cada estado final a los estados finales del AFD 
            afd.agregar_estado_final(estado_final.strip()) # Agrega el estado final al AFD 
        label_estado_actual.config(text=f"Estado inicial: {estado_inicial}, Estados finales: {estados_finales}") # Actualiza la etiqueta de estado actual 
        entry_estado_inicial.delete(0, tk.END) # Limpia el campo de entrada del estado inicial 
        entry_estados_finales.delete(0, tk.END) # Limpia el campo de entrada de los estados finales 
    except ValueError as e: # Captura cualquier error que ocurra al configurar los estados 
        messagebox.showerror("Error", str(e)) # Muestra un mensaje de error si ocurre un error al configurar los estados 
    actualizar_visualizacion() # Actualiza la visualización del AFD 

def simular_cadena(): # Función para simular una cadena en el AFD 
    cadena = entry_cadena.get() # Obtiene la cadena ingresada en el campo de entrada
    if not cadena: # Verifica si la cadena no está ingresada 
        messagebox.showwarning("Advertencia", "Ingrese la palabra a simular.") # Muestra un mensaje de advertencia si no se ingresa una palabra 
        return # Retorna para salir de la función

    if afd.estado_inicial is None or not afd.estados_finales: # Verifica si el estado inicial o los estados finales no están configurados
        messagebox.showwarning("Advertencia", "Debe configurar el estado inicial y los estados finales antes de simular.") # Muestra un mensaje de advertencia si no se han configurado los estados necesarios
        return # Retorna para salir de la función

    es_aceptada = afd.aceptar(cadena) # Verifica si la cadena es aceptada por el AFD
    if es_aceptada: # Verifica si la cadena es aceptada
        messagebox.showinfo("Resultado", f"La palabra '{cadena}' es ACEPTADA por el AFD.") 
    else:
        messagebox.showinfo("Resultado", f"La palabra '{cadena}' NO es aceptada por el AFD.")
    entry_cadena.delete(0, tk.END)




def dibujar_estado(canvas, x, y, nombre, es_inicial, es_final): # Función para dibujar un estado en el canvas 
    radio = 30 # Radio del círculo del estado
    canvas.create_oval(x - radio, y - radio, x + radio, y + radio, outline='white') # Dibuja el círculo del estado
    fuente_estado = ('Helvetica', 15) # Fuente para el nombre del estado 
    fuente_transiciones = ('Helvetica', 12, 'bold') 
    # Usar estas fuentes al crear textos en el canvas
    canvas.create_text(x, y, text=nombre, font=fuente_transiciones, fill='white') # Dibuja el nombre del estado
    if es_inicial: # Verifica si el estado es el estado inicial
        canvas.create_line(x - radio * 2, y, x - radio, y, arrow=tk.LAST, fill='white') # Dibuja la flecha indicando el estado inicial
    if es_final:
        canvas.create_oval(x - radio + 5, y - radio + 5, x + radio - 5, y + radio - 5, outline='white') # Dibuja un círculo más pequeño para indicar el estado final




def dibujar_transicion(canvas, x1, y1, x2, y2, simbolo, estado_origen, estado_destino, lados_transiciones, angulo_offset=0, color="white"): # Función para dibujar una transición en el canvas
    radio = 20 # Radio del círculo de la transición
    if estado_origen == estado_destino:  # Verifica si es un bucle
        # Coordenadas para el arco circular que forma el bucle
        arc_start = 30  # Ángulo de inicio
        arc_extent = 300  # Extensión del arco
        bucle_size = 30  # Ajusta al tamaño del bucle
        canvas.create_arc(x1 - bucle_size, y1 - bucle_size, x1 + bucle_size, y1 + bucle_size,
                          start=arc_start, extent=arc_extent, style=tk.ARC, outline=color, width=2) # Dibuja el arco del bucle 
        # Ubicación del símbolo para el bucle
        canvas.create_text(x1 + bucle_size + 10, y1 - 10, text=simbolo, fill=color) # Dibuja el símbolo del bucle 
        # Dibuja una flecha al final del arco para indicar dirección
        angle_rad = math.radians(arc_start + arc_extent) # Ángulo de la flecha en radianes 
        arrow_x = x1 + bucle_size * math.cos(angle_rad) # Coordenada x de la flecha 
        arrow_y = y1 - bucle_size * math.sin(angle_rad) # Coordenada y de la flecha
        canvas.create_line(arrow_x, arrow_y, arrow_x + 5, arrow_y + 5, arrow=tk.LAST, fill=color) # Dibuja la flecha al final del arco 
    else:
        # Cálculo de transiciones normales (No bucles)
        angulo = math.atan2(y2 - y1, x2 - x1) + angulo_offset # Cálculo del ángulo de la transición 
        distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) # Cálculo de la distancia entre los estados 
        curva = distancia / 3 # Cálculo de la curva de la transición 

        control_x = (x1 + x2) / 2 + curva * math.sin(angulo) # Cálculo de la coordenada x del punto de control de la curva 
        control_y = (y1 + y2) / 2 - curva * math.cos(angulo) # Cálculo de la coordenada y del punto de control de la curva 

        canvas.create_line(x1, y1, control_x, control_y, x2, y2,
                           smooth=True, arrow=tk.LAST, fill=color) # Dibuja la transición con una curva suave y una flecha al final 
        canvas.create_text(control_x, control_y, text=simbolo, fill=color) # Dibuja el símbolo de la transición en el punto de control 





def actualizar_visualizacion(): # Función para actualizar la visualización del AFD en el canvas
    datos_afd = afd.obtener_datos_visuales() # Obtiene los datos visuales del AFD 
    canvas.delete("all")  # Limpia el canvas

    # Calcula el punto de inicio para centrar los dibujos en el canvas
    canvas_width = canvas.winfo_width()  # Obtiene el ancho del canvas
    canvas_height = canvas.winfo_height()  # Obtiene el alto del canvas
    num_estados = len(datos_afd['estados'])
    step = 150  # Paso entre estados. Ajusta según sea necesario.
    # Centra horizontalmente
    initial_x = (canvas_width - step * (num_estados - 1)) // 2 if num_estados > 1 else canvas_width // 2
    # Centra verticalmente
    initial_y = canvas_height // 2

    # Inicializa el registro de lados de transiciones para los estados actuales 
    lados_transiciones = {estado: {'derecho': False, 'izquierdo': False} for estado in datos_afd['estados']} # Inicializa los lados de las transiciones para cada estado 

    posiciones = {}

    # Dibuja los estados de forma horizontal y centrados
    for i, estado in enumerate(sorted(datos_afd['estados'])): # Itera sobre los estados ordenados
        es_inicial = estado == datos_afd['estado_inicial'] # Verifica si el estado es el estado inicial 
        es_final = estado in datos_afd['estados_finales'] # Verifica si el estado es un estado final 
        posiciones[estado] = (initial_x + i * step, initial_y)  # Guarda la posición del estado
        dibujar_estado(canvas, *posiciones[estado], estado, es_inicial, es_final)  # Dibuja el estado

    # Dibuja las transiciones
    for origen, trans in datos_afd['transiciones'].items(): # Itera sobre las transiciones de los estados 
        x1, y1 = posiciones[origen] # Obtiene la posición del estado origen 
        for simbolo, destino in trans.items(): # Itera sobre los símbolos y estados destino de las transiciones 
            x2, y2 = posiciones[destino] # Obtiene la posición del estado destino 
            dibujar_transicion(canvas, x1, y1, x2, y2, simbolo, origen, destino, lados_transiciones) # Dibuja la transición 

    # Reinicia los lados de las transiciones después de dibujarlas
    for estado in datos_afd['estados']: # Itera sobre los estados 
        lados_transiciones[estado] = {'derecho': False, 'izquierdo': False} # Reinicia los lados de las transiciones para cada estado 


# Inicialización de la interfaz gráfica
root = tk.Tk()
#titulo con estilo de letra
root.title("Simulador de AFD")

# Frame para el área de visualización del AFD
frame_canvas = tk.Frame(root, bg='#F7C4A5', bd=10, relief=tk.RIDGE)
frame_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#BURDEDO= bg='#7C1034'
#CELESTE= bg='#CFE5FF'
# Crea el Canvas dentro del frame para el área de visualización
canvas = tk.Canvas(frame_canvas, width=800, height=800, bg='#4D4861')
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#canvas es para dibujar los estados y transiciones del autómata
letra = ('Times new Roman', 12) 
titulo= ('Times new Roman', 15, 'underline')
label_transiciones = tk.Label(root, text="Transiciones:", font=titulo, fg='#36454F')
 

label_transiciones.pack()
#label es para poner texto en la interfaz gráfica  

frame_transiciones = tk.Frame(root, padx=15, pady=10 )#esta linea deja un espacio entre los elementos
frame_transiciones.pack(padx=10, pady=10, fill=tk.X) 

label_estado_origen = tk.Label(frame_transiciones, text="Estado origen:", font=letra, fg='#36454F')
label_estado_origen.pack(side=tk.LEFT) #esta linea es para que el label se vea en la interfaz gráfica
entry_estado_origen = tk.Entry(frame_transiciones, font=letra, width=10, bg='#fdcae1')
entry_estado_origen.pack(side=tk.LEFT)

label_simbolo = tk.Label(frame_transiciones, text="Símbolo:", font=letra, fg='#36454F') #crea un label con el texto "Símbolo:" y el estilo de letra
label_simbolo.pack(side=tk.LEFT)
entry_simbolo = tk.Entry(frame_transiciones, width=10, font=letra, bg='#fdcae1')
entry_simbolo.pack(side=tk.LEFT) 

label_estado_destino = tk.Label(frame_transiciones, text="Estado destino:", font=letra, fg='#36454F')
label_estado_destino.pack(side=tk.LEFT)
entry_estado_destino = tk.Entry(frame_transiciones, width=10, font=letra, bg='#fdcae1')
entry_estado_destino.pack(side=tk.LEFT)

button_agregar_transicion = tk.Button(root, text="Agregar Transición", command=agregar_transicion, font=letra,  bg="#36454F", fg="#FFFFFF") 
button_agregar_transicion.pack(pady=5)

button_eliminar_transicion = tk.Button(root, text="Eliminar Transición", command=eliminar_transicion, font=letra, bg="#36454F", fg="#FFFFFF")
button_eliminar_transicion.pack(pady=5)

listbox_transiciones = tk.Listbox(root, bg='#fdcae1', font=letra)
label_estado_inicial = tk.Label(root, text="Estado Inicial:", font=letra, fg='#36454F')
listbox_transiciones.pack()

label_estado_inicial = tk.Label(root, text="Estado Inicial:", font=letra, fg='#36454F')
label_estado_inicial.pack()
entry_estado_inicial = tk.Entry(root, bg='#fdcae1', font=letra)
entry_estado_inicial.pack()

label_estados_finales = tk.Label(root, text="Estados Finales (separados por comas):", font=letra, fg='#36454F')
label_estados_finales.pack()
entry_estados_finales = tk.Entry(root, bg='#fdcae1', font=letra)
entry_estados_finales.pack()

button_configurar_estados = tk.Button(root, text="Ingresar los Estados", command=configurar_estados, font=letra,  bg="#36454F", fg="#FFFFFF")
button_configurar_estados.pack(pady=10)

label_estado_actual = tk.Label(root, text="Estado Inicial: None, Estados finales: None", font=letra, fg='#36454F')
label_estado_actual.pack(pady=10)

label_cadena = tk.Label(root, text="Ingrese la Palabra a Simular:", font=titulo, fg='#36454F')
label_cadena.pack()
entry_cadena = tk.Entry(root, font=letra, bg='#fdcae1')
entry_cadena.pack()

button_simular_cadena = tk.Button(root, text="Simular Palabra", command=simular_cadena, font=letra, fg='#36454F')
button_simular_cadena.configure(bg="#36454F", fg="#FFFFFF")
button_simular_cadena.pack()

afd = AFD()
actualizar_visualizacion() 

root.mainloop()