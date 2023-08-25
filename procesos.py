import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from dotenv import load_dotenv

class ProcedimientosApp:
    def __init__(self, window, db_configurations):
        self.window = window
        self.window.title('Seguimiento de los procesos')
        self.window.geometry("900x600")
        
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(pady=20, padx=20, fill='both', expand=True)
        
        for db_name, db_info in db_configurations.items():
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=db_info['tab_text'])
            self.create_tab_content(tab, db_name, db_info)
    
    def create_tab_content(self, tab, db_name, db_info):
        frame = tk.LabelFrame(tab, text=db_info['frame_text'])
        frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        for button_text, action in db_info['buttons']:
            button = ttk.Button(frame, text=button_text, command=action)
            button.pack(pady=10, padx=20, fill='both', expand=True)
        
        result_label = tk.Label(frame, text='', anchor="w")
        result_label.pack(padx=10, pady=10)
        
        tree = ttk.Treeview(frame, height=10, columns=("Process",))
        tree.column("#0", width=0, stretch="NO")
        tree.column("Process", anchor="w", width=500)
        tree.pack(padx=10, pady=10, fill='both', expand=True)
        
        tree.bind("<ButtonRelease-1>", self.selected_item)
        result_label.configure(text='Sin Conexión...')
        
        # Configure other widgets and actions as needed
       
    


    def execute_stored_procedure(self):
        self.result_label1.configure(text='Conectando...')

        # Crea una conexión con la base de datos
        try:
            conn = mysql.connector.connect(
                host=self.server_test,
                user=self.db_user,
                password=self.db_password,
                database=self.test_db_name
            )
            self.result_label1.configure(text='Conexión exitosa Servidor Test')
        except mysql.connector.Error as error:
            self.result_label1.configure(text=f'Error al conectar a la base de datos: {error}', wraplength=500)
            return

        # Crea una instancia del cursor
        cursor = conn.cursor()

        # Ejecuta el procedimiento almacenado
        cursor.callproc('check_proceso_activo')

        # Recupera los resultados del procedimiento almacenado
        results = cursor.stored_results()
        output = [tuple(row) for row in results][0]

            
        # Limpiar el Treeview
        self.tree1.delete(*self.tree1.get_children())

        # Configurar las columnas en el Treeview
        self.tree1['columns'] = ('Process',)
        self.tree1.column("#0", width=0, stretch="NO")
        self.tree1.column("Process", anchor="w", width=500)
        self.tree1.heading("Process", text="Procesos Activos")

        # Mostrar los resultados en el Treeview
        cont=1
        for item in output:
            self.tree1.insert("", tk.END, text="", values=(f"{cont}) {item}",))
            cont+=1            

        # Cierra la conexión
        conn.close()
       
        # Ajustar el tamaño de la columna para que se expanda y llene el espacio disponible
        self.tree1.column("Process", width=self.tree1.winfo_width())

        # Empaqueta el Treeview para expandirlo
        self.tree1.pack(padx=10, pady=10, fill='both', expand=True)
    
    def metropolis_test(self):
        self.result_label1.configure(text='Conectando...')
        # Crea una conexión con la base de datos
        try:
            conn = psycopg2.connect(
                host=self.server_test,
                user='postgres',
                password=self.db_password,
                dbname='metropolis'
            )
            self.result_label1.configure(text='Conexión exitosa Servidor Test Metropolis')
        except psycopg2.Error as error:
            self.result_label1.configure(text=f'Error al conectar a la base de datos: {error}', wraplength=500)
            return
        # Crea una instancia del cursor
        cursor = conn.cursor()
        # Ejecuta la consulta
        cursor.execute('''SELECT p.id, emi.nombre_fantasia, emisor_id, fecha_hora_inicio, estado, cant_documentos 
            FROM public.proc_proceso p
            inner join public.app_emisor emi on emi.id = emisor_id
            where estado not in ('FINALIZADO', 'FINALIZADO_ERROR')            
            order by id desc''')

        # Recupera los resultados de la consulta
        results = cursor.fetchall()

        # Mostrar el resultado en el Treeview
        self.tree1.delete(*self.tree1.get_children())
        # Configurar las columnas en el Treeview
        self.tree1['columns'] = ('ID', 'Nombre Fantasia', 'Emisor ID', 'Fecha/Hora Inicio', 'Estado', 'Cant Doc.')
        self.tree1.heading('#0', text='', anchor='w')
        self.tree1.column('#0', width=0, stretch=tk.NO)

        # Configurar tamaños de las columnas
        self.tree1.column('ID', width=50)
        self.tree1.column('Emisor ID', width=60)
        self.tree1.column('Cant Doc.', width=60)
        


        for column in self.tree1['columns']:
            self.tree1.heading(column, text=column)
            self.tree1.column(column, anchor='center')
        
        for row in results:
            # Insertar las columnas en el Treeview
            self.tree1.insert("", tk.END, text="", values=row)


        # Cierra la conexión
        conn.close()

    def respuestaSET_test(self):
        self.result_label1.configure(text='Conectando...')
        # Crea una conexión con la base de datos
        try:
            conn = psycopg2.connect(
                host=self.server_test,
                user='postgres',
                password=self.db_password,
                dbname='metropolis'
            )
            self.result_label1.configure(text='Conexión exitosa Servidor Test Verificando respuesta de la SET')
        except psycopg2.Error as error:
            self.result_label1.configure(text=f'Error al conectar a la base de datos: {error}', wraplength=500)
            return
        # Crea una instancia del cursor
        cursor = conn.cursor()
        # Ejecuta la consulta
        cursor.execute('''select emi.nombre_fantasia ,ars.fecha_hora , ars.proceso_id, ars.resultado, categoria  from app_respuesta_set ars
            inner join public.proc_proceso p on p.id = ars.proceso_id 
            inner join public.app_emisor emi on emi.id = emisor_id 
            order by fecha_hora desc limit 100;''')

        # Recupera los resultados de la consulta
        results = cursor.fetchall()

        # Mostrar el resultado en el Treeview
        self.tree1.delete(*self.tree1.get_children())
        # Configurar las columnas en el Treeview
        self.tree1['columns'] = ('ID','Cliente', 'fecha_hora', 'proceso_id', 'resultado','categoria')
        self.tree1.heading('#0', text='', anchor='w')
        self.tree1.column('#0', width=0, stretch=tk.NO)

        # # Configurar tamaños de las columnas
        self.tree1.column('ID', width=10)
        self.tree1.column('resultado', stretch=tk.YES)
        # self.tree1.column('Cant Doc.', width=60)      


        for column in self.tree1['columns']:            
            self.tree1.heading(column, text=column)
            self.tree1.column(column, anchor='center')
        
                       
        cont=1
        for row in results:
            # Insertar las columnas en el Treeview
            self.tree1.insert("", tk.END, values=(cont, *row))
            cont+=1            
        
        self.tree1.bind("<ButtonRelease-1>", self.mostrar_info_fila)
        # Cierra la conexión
        conn.close()

    def mostrar_info_fila(self, event):
        # Verificar si la ventana de información ya está abierta
        if hasattr(self, 'info_window') and self.info_window.winfo_exists():
            # Si la ventana existe, actualizar los valores y salir
            self.info_entry.delete(0, tk.END)
            self.info_entry.insert(tk.END, values)
            return

        # Obtener el índice de la fila seleccionada
        selected_item = self.tree1.selection()[0]
        # Obtener los valores de la fila seleccionada
        self.values = self.tree1.item(selected_item)['values'][4]

        # Crear la ventana de información
        self.info_window = tk.Toplevel(self.wind)
        self.info_window.geometry("240x300")
        self.info_window.title('Respuesta de la SET')

        # Crear un Entry para mostrar los valores
        self.info_entry = tk.Entry(self.info_window, width=50)
        self.info_entry.pack(padx=10, pady=10, fill='both', expand=True)

        # Mostrar los valores en el Entry
        self.info_entry.insert(tk.END, self.values)

        # Permitir copiar el contenido del Entry
        self.info_entry.configure(state='readonly')

        # Hacer que la ventana principal no sea accesible mientras se muestra la ventana de información
        self.wind.grab_set()

        # Manejar el evento de cierre de la ventana de información
        self.info_window.protocol("WM_DELETE_WINDOW", self.cerrar_info_fila)

    def cerrar_info_fila(self):
        # Liberar el bloqueo de la ventana principal
        self.wind.grab_release()
        # Cerrar la ventana de información
        self.info_window.destroy()


    def selected_item(self, event):
        selection = event.widget.selection()
        for selected in selection:
            item = event.widget.item(selected, 'values')[0]
            print(item)


def main():
    load_dotenv()
    
    db_configurations = {
        'test_db': {
            'tab_text': 'Test',
            'frame_text': 'Ver procesos Activos',
            'buttons': [('Procesos Activos', self.execute_stored_procedure), ('Metropolis', None), ('Respuesta de la SET', None)],
            'db_server': os.getenv('SERVER_TEST'),
            'db_user': os.getenv('DB_USER'),
            'db_password': os.getenv('DB_PASSWORD'),
            'db_name': os.getenv('TEST_DB_NAME'),
        },
        'produccion_db': {
            'tab_text': 'Producción',
            'frame_text': 'Ver procesos Activos',
            'buttons': [('Procesos Activos', None), ('Metropolis', None), ('Respuesta de la SET', None)],
            'db_server': os.getenv('SERVER_TEST'),
            'db_user': os.getenv('DB_USER'),
            'db_password': os.getenv('DB_PASSWORD'),
            'db_name': os.getenv('TEST_DB_NAME'),
        },
        # Add more configurations for other databases
    }
    
    root = tk.Tk()
    app = ProcedimientosApp(root, db_configurations)
    
    icon_path = "images/favicon.ico"
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(True, icon_photo)
    
    root.mainloop()

if __name__ == '__main__':
    main()
