import os
import mysql.connector
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk
import psycopg2
from PIL import Image, ImageTk



class Procedimientos:
    def __init__(self, windows, server_test, server_prod, server_claro, db_user, db_password, db_name, test_db_name):
        self.wind = windows
        self.wind.title('Seguimiento de los procesos')
        self.wind.geometry("900x600")
        self.server_test = server_test
        self.server_prod = server_prod
        self.server_claro = server_claro        
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.test_db_name = test_db_name
    
        # Creating a Notebook Container
        self.notebook = ttk.Notebook(self.wind)
        self.notebook.pack(pady=20, padx=20, fill='both', expand=True)

        # Create tabs
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        # Agregamos los tabs al notebook
        self.notebook.add(self.tab1, text="Test")
        self.notebook.add(self.tab2, text='Producción')
        self.notebook.add(self.tab3, text='Claro')

        # Tab 1
        frame1 = tk.LabelFrame(self.tab1, text='Ver procesos Activos')
        frame1.pack(pady=20, padx=20, fill='both', expand=True)

        button1 = ttk.Button(frame1, text='Procesos Activos', command=self.execute_stored_procedure)
        button1.pack(pady=10,padx=20, fill='both', expand=True)
        butt1 = ttk.Button(frame1, text='Metropolis', command=self.metropolis_test)
        butt1.pack(pady=10, padx=20, fill='both', expand=True)
        btn1 = ttk.Button(frame1, text='Respuesta de la SET', command=self.respuestaSET_test)
        btn1.pack(pady=10, padx=20, fill='both', expand=True)
        

        # Agregar Label para mostrar resultado de la conexión
        self.result_label1 = tk.Label(frame1, text='', anchor="w")
        self.result_label1.pack(padx=10, pady=10)

        self.tree1 = ttk.Treeview(frame1, height=10, columns=("Process",))
        self.tree1.column("#0", width=0, stretch="NO")
        self.tree1.column("Process", anchor="w", width=500)
        self.tree1.pack(padx=10, pady=10, fill='both', expand=True)

        self.tree1.bind("<ButtonRelease-1>", self.selected_item)
      
        self.result_label1.configure(text='Sin Conexión...')

        # Tab 2
        frame2 = tk.LabelFrame(self.tab2, text='Ver procesos Activos')
        frame2.pack(pady=20, padx=20, fill='both', expand=True)
        button2 = ttk.Button(frame2, text='Procesos Activos', command=self.execute_stored_procedure_prod)
        button2.pack(pady=10, padx=20, fill='both', expand=True)
              
        butt2 = ttk.Button(frame2, text='Metropolis', command=self.metropolis_prod)
        butt2.pack(pady=10, padx=20, fill='both', expand=True)
        
        btn2 = ttk.Button(frame2, text='Respuesta de la SET', command=self.respuestaSET_prod)
        btn2.pack(pady=10, padx=20, fill='both', expand=True)
         
          # Agregar Label para mostrar resultado de la conexión
        self.result_label2 = tk.Label(frame2, text='', anchor="w")
        self.result_label2.pack(padx=10, pady=10)

        self.tree2 = ttk.Treeview(frame2, height=10, columns=("Process",))
        self.tree2.column("#0", width=0, stretch="NO")
        self.tree2.column("Process", anchor="w", width=500)
        self.tree2.pack(padx=10, pady=10, fill='both', expand=True)

        self.tree2.bind("<ButtonRelease-1>", self.selected_item)
        self.result_label2.configure(text='Sin Conexión...')

        # Tab 3
        frame3 = tk.LabelFrame(self.tab3, text='Ver procesos Activos')
        frame3.pack(pady=20, padx=20, fill='both', expand=True)

        button3 = ttk.Button(frame3, text='Procesos Activos', command=self.execute_stored_procedure_claro)
        button3.pack(pady=10,padx=20, fill='both', expand=True)

        # butt3 = ttk.Button(frame3, text='Metropolis', command=self.metropolis_claro)
        # butt3.pack(pady=10, padx=20, fill='both', expand=True)
        

        # Agregar Label para mostrar resultado de la conexión
        self.result_label3 = tk.Label(frame3, text='', anchor="w")
        self.result_label3.pack(padx=10, pady=10)

        self.tree3 = ttk.Treeview(frame3, height=10, columns=("Process",))
        self.tree3.column("#0", width=0, stretch="NO")
        self.tree3.column("Process", anchor="w", width=500)
        self.tree3.pack(padx=10, pady=10, fill='both', expand=True)

        self.tree3.bind("<ButtonRelease-1>", self.selected_item)
        self.result_label3.configure(text='Sin Conexión...')

    def execute_stored_procedure_claro(self):
        self.result_label3.configure(text='Conectando...')

        # Crea una conexión con la base de datos
        try:
            conn = mysql.connector.connect(
                host=self.server_claro,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            self.result_label3.configure(text='Conexión exitosa Servidor Claro')
        except mysql.connector.Error as error:
            self.result_label3.configure(text=f'Error al conectar a la base de datos: {error}', wraplength=500)
            return

        # Crea una instancia del cursor
        cursor = conn.cursor()

        # Ejecuta el procedimiento almacenado
        cursor.callproc('check_proceso_activo')

        # Recupera los resultados del procedimiento almacenado
        results = cursor.stored_results()
        output = [tuple(row) for row in results][0]

        # Mostrar el resultado en el Treeview
        self.tree3.delete(*self.tree3.get_children())

        i = '"No hay procesos activos, está listo para reiniciar los servicios!"'
        if not output:
            self.tree3.insert("", tk.END, text="", values=(i,))
        else:
            for item in output:
                self.tree3.insert("", tk.END, text="", values=(item,))

        # Cierra la conexión
        conn.close()
    
    def metropolis_claro(self):
        self.result_label3.configure(text='Conectando...')
        # Crea una conexión con la base de datos
        try:
            conn = psycopg2.connect(
                host=self.server_claro,
                user='postgres',
                password=self.db_password,
                dbname='metropolis'
            )
            self.result_label3.configure(text='Conexión exitosa Servidor Claro Metropolis')
        except psycopg2.Error as error:
            self.result_label3.configure(text=f'Error al conectar a la base de datos: {error}', wraplength=500)
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
        self.tree3.delete(*self.tree3.get_children())
       # ...

        # Configurar las columnas en el Treeview
        self.tree3['columns'] = ('ID', 'Nombre Fantasia', 'Emisor ID', 'Fecha/Hora Inicio', 'Estado', 'Cant Documentos')
        self.tree3.heading('#0', text='', anchor='w')
        self.tree3.column('#0', width=0, stretch=tk.NO)

        for column in self.tree3['columns']:
            self.tree3.heading(column, text=column)
            self.tree3.column(column, anchor='center')

        # ...

        for row in results:
            # Insertar las columnas en el Treeview
            self.tree3.insert("", tk.END, text="", values=row)


        # Cierra la conexión
        conn.close()

##################  PROD

    def execute_stored_procedure_prod(self):
        self.result_label2.configure(text='Conectando...')

        # Crea una conexión con la base de datos
        try:
            conn = mysql.connector.connect(
                host=self.server_prod,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            self.result_label2.configure(text='Conexión exitosa Servidor Multi Producción')
        except mysql.connector.Error as error:
            self.result_label2.configure(text=f'Error al conectar a la base de datos: {error}', wraplength=500)
            return

        # Crea una instancia del cursor
        cursor = conn.cursor()

        # Ejecuta el procedimiento almacenado
        cursor.callproc('check_proceso_activo')

        # Recupera los resultados del procedimiento almacenado
        results = cursor.stored_results()
        output = [tuple(row) for row in results][0]

        # Mostrar el resultado en el Treeview
        self.tree2.delete(*self.tree2.get_children())

            
        # Limpiar el Treeview
        self.tree2.delete(*self.tree2.get_children())

        # Configurar las columnas en el Treeview
        self.tree2['columns'] = ('Process',)
        self.tree2.column("#0", width=0, stretch="NO")
        self.tree2.column("Process", anchor="w", width=500)
        self.tree2.heading("Process", text="Procesos Activos")    

        i = '"No hay procesos activos, está listo para reiniciar los servicios!"'
        if not output:
            self.tree2.insert("", tk.END, text="", values=(i,))
        else:
            cont=1
            for item in output:
                self.tree2.insert("", tk.END, text="", values=(f"{cont}) {item}",))
                cont+=1            
       
        # Cierra la conexión
        conn.close()
        
        # Ajustar el tamaño de la columna para que se expanda y llene el espacio disponible
        self.tree2.column("Process", width=self.tree2.winfo_width())

        # Empaqueta el Treeview para expandirlo
        self.tree2.pack(padx=10, pady=10, fill='both', expand=True)
    
    def metropolis_prod(self):
        self.result_label2.configure(text='Conectando...')
        # Crea una conexión con la base de datos
        try:
            conn = psycopg2.connect(
                host=self.server_prod,
                user='postgres',
                password=self.db_password,
                dbname='metropolis'
            )
            self.result_label2.configure(text='Conexión exitosa Servidor Multi Producción')
        except psycopg2.Error as error:
            self.result_label2.configure(text=f'Error al conectar a la base de datos: {error}', wraplength=500)
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
        self.tree2.delete(*self.tree2.get_children())
       # ...

        # Configurar las columnas en el Treeview
        self.tree2['columns'] = ('ID', 'Nombre Fantasia', 'Emisor ID', 'Fecha/Hora Inicio', 'Estado', 'Cant Doc.')
        self.tree2.heading('#0', text='', anchor='w')
        self.tree2.column('#0', width=0, stretch=tk.NO)

        
        # Configurar tamaños de las columnas
        self.tree2.column('ID', width=50)
        self.tree2.column('Emisor ID', width=60)
        self.tree2.column('Cant Doc.', width=60)
        
        for column in self.tree2['columns']:
            self.tree2.heading(column, text=column)
            self.tree2.column(column, anchor='center')
       
        for row in results:
            # Insertar las columnas en el Treeview
            self.tree2.insert("", tk.END, text="", values=row)


        # Cierra la conexión
        conn.close()
    
    def respuestaSET_prod(self):
        self.result_label2.configure(text='Conectando...')
        # Crea una conexión con la base de datos
        try:
            conn = psycopg2.connect(
                host=self.server_prod,
                user='postgres',
                password=self.db_password,
                dbname='metropolis'
            )
            self.result_label2.configure(text='Conexión exitosa Servidor MultiProd Verificando respuesta de la SET')
        except psycopg2.Error as error:
            self.result_label2.configure(text=f'Error al conectar a la base de datos: {error}', wraplength=500)
            return
        # Crea una instancia del cursor
        cursor = conn.cursor()
        # Ejecuta la consulta
        cursor.execute('''SELECT emi.nombre_fantasia, ars.fecha_hora, ars.proceso_id,  ars.resultado, categoria
        FROM app_respuesta_set ars 
        INNER JOIN public.proc_proceso p ON p.id = ars.proceso_id
        INNER JOIN public.app_emisor emi ON emi.id = p.emisor_id 
        INNER JOIN ( SELECT MAX(fecha_hora) AS ultima_fecha, p.emisor_id
            FROM app_respuesta_set ars
            INNER JOIN public.proc_proceso p ON p.id = ars.proceso_id
            --AND ars.fecha_hora  > CURRENT_TIMESTAMP - INTERVAL '48 hours'
            GROUP BY p.emisor_id
        ) ultima_fecha_emisor ON ars.fecha_hora = ultima_fecha_emisor.ultima_fecha AND p.emisor_id = ultima_fecha_emisor.emisor_id
        where p.estado not in ('FINALIZADO', 'FINALIZADO_ERROR')
        ORDER BY ars.fecha_hora desc;''')

        # Recupera los resultados de la consulta
        results = cursor.fetchall()

        # Mostrar el resultado en el Treeview
        self.tree2.delete(*self.tree2.get_children())
        # Configurar las columnas en el Treeview
        self.tree2['columns'] = ('ID','Cliente', 'fecha_hora', 'proceso_id', 'resultado','categoria')
        self.tree2.heading('#0', text='', anchor='w')
        self.tree2.column('#0', width=0, stretch=tk.NO)

        # # Configurar tamaños de las columnas
        self.tree2.column('ID', width=10)
        self.tree2.column('resultado', stretch=tk.YES)
        # self.tree1.column('Cant Doc.', width=60)      


        for column in self.tree2['columns']:            
            self.tree2.heading(column, text=column)
            self.tree2.column(column, anchor='center')
        
                       
        cont=1
        for row in results:
            # Insertar las columnas en el Treeview
            self.tree2.insert("", tk.END, values=(cont, *row))
            cont+=1            
        
        self.tree2.bind("<ButtonRelease-1>", self.mostrar_info_fila_prod)
        # Cierra la conexión
        conn.close()


    def mostrar_info_fila_prod(self, event):
       # Verificar si la ventana de información ya está abierta
        if hasattr(self, 'info_window') and self.info_window.winfo_exists():
            # Si la ventana existe, actualizar los valores y salir
            self.info_text.configure(state='normal')
            self.info_text.delete('1.0', tk.END)
            self.info_text.insert(tk.END, self.values)
            self.info_text.configure(state='disabled')
            return

        # Obtener el índice de la fila seleccionada
        selected_item = self.tree2.selection()[0]
        # Obtener los valores de la fila seleccionada
        self.values = self.tree2.item(selected_item)['values'][4]

        # Crear la ventana de información
        self.info_window = tk.Toplevel(self.wind)
        self.info_window.title('Respuesta de la SET')

        # Crear un widget Text para mostrar los valores
        self.info_text = tk.Text(self.info_window, wrap=tk.WORD)
        self.info_text.pack(padx=10, pady=10, fill='both', expand=True)

        self.info_text.insert(tk.END, self.values)
        self.info_text.configure(state='disabled')

        # Agregar un control de desplazamiento vertical
        scrollbar = tk.Scrollbar(self.info_window, command=self.info_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text.config(yscrollcommand=scrollbar.set)

        # Ajustar el tamaño de la ventana de información al contenido
        self.info_window.update_idletasks()
        width = self.info_window.winfo_reqwidth()
        height = self.info_window.winfo_reqheight()
        self.info_window.geometry(f"{width}x{height}")

        # Hacer que la ventana principal no sea accesible mientras se muestra la ventana de información
        self.wind.grab_set()

        # Manejar el evento de cierre de la ventana de información
        self.info_window.protocol("WM_DELETE_WINDOW", self.cerrar_info_fila)

##################    TEST
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
        cursor.execute('''SELECT emi.nombre_fantasia, ars.fecha_hora, ars.proceso_id,  ars.resultado, categoria
        FROM app_respuesta_set ars 
        INNER JOIN public.proc_proceso p ON p.id = ars.proceso_id
        INNER JOIN public.app_emisor emi ON emi.id = p.emisor_id 
        INNER JOIN ( SELECT MAX(fecha_hora) AS ultima_fecha, p.emisor_id
            FROM app_respuesta_set ars
            INNER JOIN public.proc_proceso p ON p.id = ars.proceso_id
            --AND ars.fecha_hora  > CURRENT_TIMESTAMP - INTERVAL '48 hours'
            GROUP BY p.emisor_id
        ) ultima_fecha_emisor ON ars.fecha_hora = ultima_fecha_emisor.ultima_fecha AND p.emisor_id = ultima_fecha_emisor.emisor_id
        where p.estado not in ('FINALIZADO', 'FINALIZADO_ERROR')
        ORDER BY ars.fecha_hora desc;''')

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
            self.info_text.configure(state='normal')
            self.info_text.delete('1.0', tk.END)
            self.info_text.insert(tk.END, self.values)
            self.info_text.configure(state='disabled')
            return

        # Obtener el índice de la fila seleccionada
        selected_item = self.tree1.selection()[0]
        # Obtener los valores de la fila seleccionada
        self.values = self.tree1.item(selected_item)['values'][4]

        # Crear la ventana de información
        self.info_window = tk.Toplevel(self.wind)
        self.info_window.title('Respuesta de la SET')

        # Crear un widget Text para mostrar los valores
        self.info_text = tk.Text(self.info_window, wrap=tk.WORD)
        self.info_text.pack(padx=10, pady=10, fill='both', expand=True)

        self.info_text.insert(tk.END, self.values)
        self.info_text.configure(state='disabled')

        # Agregar un control de desplazamiento vertical
        scrollbar = tk.Scrollbar(self.info_window, command=self.info_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text.config(yscrollcommand=scrollbar.set)

        # Ajustar el tamaño de la ventana de información al contenido
        self.info_window.update_idletasks()
        width = self.info_window.winfo_reqwidth()
        height = self.info_window.winfo_reqheight()
        self.info_window.geometry(f"{width}x{height}")

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
    # Carga las variables de entorno desde el archivo .env
    load_dotenv()
    server_prod = os.getenv('SERVER_PROD')
    server_test = os.getenv('SERVER_TEST')
    server_claro = os.getenv('SERVER_CLARO')    
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    test_db_name = os.getenv('TEST_DB_NAME')


    # Crea una instancia de la clase Procedimientos
    root = tk.Tk()
    app = Procedimientos(root, server_test, server_prod, server_claro, db_user, db_password, db_name, test_db_name)
    
    #configuración del icono
    # Ruta de la imagen del ícono
    icon_path = "images/favicon.ico"

    # Carga la imagen del ícono
    icon_image = Image.open(icon_path)

    # Convierte la imagen en un objeto PhotoImage
    icon_photo = ImageTk.PhotoImage(icon_image)
    
    # Establece el ícono de la ventana principal
    root.iconphoto(True, icon_photo)
    
    root.mainloop()

if __name__ == '__main__':
    main()
