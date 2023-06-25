import mysql.connector
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from datetime import datetime
import re

class Tiquet:
    def __init__(self, nombre_cliente, rut_cliente, telefono_cliente, email_cliente, tipo_tiquet, criticidad, detalle_servicio, detalle_problema, area_derivacion, ejecutivo_apertura, estado, fecha_apertura, fecha_cierre, ejecutivo_cierre):
        self.idTiquet = None  # Se asignará automáticamente al guardar en la base de datos
        self.nombre_cliente = nombre_cliente
        self.rut_cliente = rut_cliente
        self.telefono_cliente = telefono_cliente
        self.email_cliente = email_cliente
        self.tipo_tiquet = tipo_tiquet
        self.criticidad = criticidad
        self.detalle_servicio = detalle_servicio
        self.detalle_problema = detalle_problema
        self.area_derivacion = area_derivacion
        self.ejecutivo_apertura = ejecutivo_apertura
        self.estado = estado
        self.fecha_apertura = fecha_apertura
        self.fecha_cierre = fecha_cierre
        self.ejecutivo_cierre = ejecutivo_cierre

class VentanaInicioSesion(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Inicio de sesión")
        self.etiqueta_usuario = Label(self, text="Usuario:")
        self.entrada_usuario = Entry(self)
        self.etiqueta_contrasena = Label(self, text="Contraseña:")
        self.entrada_contrasena = Entry(self, show="*")
        self.boton_inicio_sesion = Button(self, text="Iniciar sesión", command=self.iniciar_sesion)
        
        self.etiqueta_usuario.pack()
        self.entrada_usuario.pack()
        self.etiqueta_contrasena.pack()
        self.entrada_contrasena.pack()
        self.boton_inicio_sesion.pack()
        
    def iniciar_sesion(self):
        usuario = self.entrada_usuario.get()
        contrasena = self.entrada_contrasena.get()
        
        # Verificar las credenciales (aquí debes implementar tu lógica de autenticación)
        if usuario == "mesa" and contrasena == "1234":
            self.master.cambiar_frame(VentanaEjecutivoMesa)
        else:
            messagebox.showerror("Error de inicio de sesión", "Credenciales incorrectas")


class VentanaEjecutivoMesa(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Interfaz Ejecutivo Mesa")

        self.boton_crear_tiquet = Button(self, text="Crear Tiquet", command=self.crear_tiquet)
        self.boton_ver_tiquets = Button(self, text="Ver Tiquets", command=self.ver_tiquets)
        self.boton_cerrar_sesion = Button(self, text="Cerrar sesión", command=self.cerrar_sesion)

        self.boton_crear_tiquet.grid(row=10, column=0, pady=10)
        self.boton_ver_tiquets.grid(row=10, column=1, pady=10)
        self.boton_cerrar_sesion.grid(row=10, column=2, pady=10)

    def crear_tiquet(self):
        self.master.cambiar_frame(VentanaCreacionTiquet)

    def ver_tiquets(self):
        self.master.cambiar_frame(VentanaTiquets)

    def cerrar_sesion(self):
        self.master.cambiar_frame(VentanaInicioSesion)


class VentanaTiquets(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Tiquets")

        self.lista_tiquets = Listbox(self)
        self.boton_volver = Button(self, text="Volver", command=self.volver)

        self.cargar_tiquets()  # Llama al método cargar_tiquets() para mostrar los tiquets

        self.lista_tiquets.pack()
        self.boton_volver.pack()

    def cargar_tiquets(self):
        # Conectar a la base de datos y obtener los tiquets
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="consultenos"
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tiquets")
        tiquets = cursor.fetchall()
        db.close()

        for tiquet in tiquets:
            self.lista_tiquets.insert(END, tiquet)  # Insertar cada tiquet en la lista

    def volver(self):
        self.master.cambiar_frame(VentanaEjecutivoMesa)


class VentanaCreacionTiquet(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Crear Tiquet")

        # Obtener fecha y hora actual
        fecha_hora_actual = datetime.now()

        # Convertir la fecha y hora actual en una cadena formateada
        fecha_hora_actual_str = fecha_hora_actual.strftime("%d/%m/%Y %H:%M")

        # Campos de tiquet
        self.etiqueta_nombre_cliente = Label(self, text="Nombre del cliente:")
        self.entrada_nombre_cliente = Entry(self)
        self.etiqueta_rut_cliente = Label(self, text="RUT del cliente:")
        self.entrada_rut_cliente = Entry(self)
        self.etiqueta_contacto_cliente = Label(self, text="Datos de contacto del cliente:")
        self.etiqueta_telefono_cliente = Label(self, text="Teléfono:")
        self.entrada_telefono_cliente = Entry(self)
        self.etiqueta_email_cliente = Label(self, text="Correo electrónico:")
        self.entrada_email_cliente = Entry(self)
        self.etiqueta_tipo_tiquet = Label(self, text="Tipo de tiquet:")
        self.tipo_tiquet_var = StringVar()
        self.combobox_tipo_tiquet = Combobox(self, textvariable=self.tipo_tiquet_var, values=["Felicitación", "Consulta", "Reclamo", "Problema"])
        self.etiqueta_criticidad = Label(self, text="Criticidad:")
        self.entrada_criticidad = Entry(self)
        self.etiqueta_detalle_servicio = Label(self, text="Detalle del servicio:")
        self.entrada_detalle_servicio = Entry(self)
        self.etiqueta_detalle_problema = Label(self, text="Detalle del problema:")
        self.entrada_detalle_problema = Entry(self)
        self.etiqueta_area_derivacion = Label(self, text="Área para derivar:")
        self.area_derivacion_var = StringVar()
        self.combobox_area_derivacion = Combobox(self, textvariable=self.area_derivacion_var, values=["Área 1", "Área 2", "Área 3", "No deriva"])
        self.etiqueta_ejecutivo_apertura = Label(self, text="Ejecutivo que abre el tiquet:")
        self.entrada_ejecutivo_apertura = Entry(self)
        self.etiqueta_estado = Label(self, text="Estado:")
        self.estado_var = StringVar()
        self.combobox_estado = Combobox(self, textvariable=self.estado_var, values=["A resolución", "Resuelto", "No aplicable"])
        self.etiqueta_fecha_apertura = Label(self, text="Fecha apertura:")
        self.entrada_fecha_apertura = Entry(self)
        self.entrada_fecha_apertura.insert(0, fecha_hora_actual_str)
        self.entrada_fecha_apertura.config(state="readonly")
        self.etiqueta_fecha_cierre = Label(self, text="Fecha cierre:")
        self.entrada_fecha_cierre = Entry(self)
        self.entrada_fecha_cierre.config(state="disabled")
        self.etiqueta_ejecutivo_cierre = Label(self, text="Ejecutivo cierre:")
        self.entrada_ejecutivo_cierre = Entry(self)
        self.entrada_ejecutivo_cierre.config(state="readonly")

        self.boton_crear_tiquet = Button(self, text="Crear Tiquet", command=self.crear_tiquet)

        # Colocar los widgets en la ventana
        self.etiqueta_nombre_cliente.grid(row=0, column=0, sticky=W)
        self.entrada_nombre_cliente.grid(row=0, column=1)
        self.etiqueta_rut_cliente.grid(row=1, column=0, sticky=W)
        self.entrada_rut_cliente.grid(row=1, column=1)
        self.etiqueta_contacto_cliente.grid(row=2, column=0, sticky=W)
        self.etiqueta_telefono_cliente.grid(row=2, column=0, sticky=W)
        self.entrada_telefono_cliente.grid(row=2, column=1)
        self.etiqueta_email_cliente.grid(row=2, column=2, sticky=W)
        self.entrada_email_cliente.grid(row=2, column=3)
        self.etiqueta_tipo_tiquet.grid(row=3, column=0, sticky=W)
        self.combobox_tipo_tiquet.grid(row=3, column=1)
        self.etiqueta_criticidad.grid(row=4, column=0, sticky=W)
        self.entrada_criticidad.grid(row=4, column=1)
        self.etiqueta_detalle_servicio.grid(row=5, column=0, sticky=W)
        self.entrada_detalle_servicio.grid(row=5, column=1)
        self.etiqueta_detalle_problema.grid(row=6, column=0, sticky=W)
        self.entrada_detalle_problema.grid(row=6, column=1)
        self.etiqueta_area_derivacion.grid(row=7, column=0, sticky=W)
        self.combobox_area_derivacion.grid(row=7, column=1)
        self.etiqueta_ejecutivo_apertura.grid(row=8, column=0, sticky=W)
        self.entrada_ejecutivo_apertura.grid(row=8, column=1)
        self.etiqueta_estado.grid(row=9, column=0, sticky=W)
        self.combobox_estado.grid(row=9, column=1)
        self.etiqueta_fecha_apertura.grid(row=10, column=0, sticky=W)
        self.entrada_fecha_apertura.grid(row=10, column=1)
        self.etiqueta_fecha_cierre.grid(row=11, column=0, sticky=W)
        self.entrada_fecha_cierre.grid(row=11, column=1)
        self.etiqueta_ejecutivo_cierre.grid(row=12, column=0, sticky=W)
        self.entrada_ejecutivo_cierre.grid(row=12, column=1)
        self.boton_crear_tiquet.grid(row=13, column=0, pady=10)

    def crear_tiquet(self):

        # Conectar a la base de datos
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="consultenos"
        )
        # Obtener los valores ingresados por el usuario
        nombre_cliente = self.entrada_nombre_cliente.get()
        rut_cliente = self.entrada_rut_cliente.get()
        telefono_cliente = self.entrada_telefono_cliente.get()
        email_cliente = self.entrada_email_cliente.get()
        tipo_tiquet = self.tipo_tiquet_var.get()
        criticidad = self.entrada_criticidad.get()
        detalle_servicio = self.entrada_detalle_servicio.get()
        detalle_problema = self.entrada_detalle_problema.get()
        area_derivacion = self.area_derivacion_var.get()
        ejecutivo_apertura = self.entrada_ejecutivo_apertura.get()
        estado = self.estado_var.get()
        fecha_apertura = self.entrada_fecha_apertura.get()
        fecha_cierre = self.entrada_fecha_cierre.get()
        ejecutivo_cierre = self.entrada_ejecutivo_cierre.get()

        # Validar los campos
        if not rut_cliente.isdigit() or len(rut_cliente) < 8 or len(rut_cliente) > 9:
            messagebox.showerror("Error de validación", "El RUT debe contener solo números y tener entre 8 y 9 dígitos")
            return

        if not telefono_cliente.isdigit() or len(telefono_cliente) != 9:
            messagebox.showerror("Error de validación", "El número de teléfono debe contener solo números y tener 9 dígitos")
            return

        if "@" not in email_cliente or not email_cliente.endswith(".com"):
            messagebox.showerror("Error de validación", "El correo electrónico no es válido")
            return

        # Aquí debes implementar la lógica para guardar el tiquet en la base de datos y generar un idTiquet único
        # Crear un cursor para ejecutar consultas
        cursor = conexion.cursor()

        # Preparar la consulta SQL con parámetros de marcadores de posición (%s)
        consulta = "INSERT INTO tiquets (nombre_cliente, rut_cliente, telefono_cliente, email_cliente, tipo_tiquet, criticidad, detalle_servicio, detalle_problema, area_derivacion, ejecutivo_apertura, estado, fecha_apertura, fecha_cierre, ejecutivo_cierre) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (nombre_cliente, rut_cliente, telefono_cliente, email_cliente, tipo_tiquet, criticidad, detalle_servicio, detalle_problema, area_derivacion, ejecutivo_apertura, estado, fecha_apertura, fecha_cierre, ejecutivo_cierre)


        # Ejecutar la consulta SQL y obtener el ID del tiquet insertado
        cursor.execute(consulta, valores)
        self.idTiquet = cursor.lastrowid

        # Confirmar los cambios en la base de datos
        conexion.commit()

        # Cerrar el cursor y la conexión a la base de datos
        cursor.close()
        conexion.close()
        # Mostrar un mensaje de éxito y limpiar los campos
        messagebox.showinfo("Tiquet creado", "El tiquet se ha creado correctamente")
        self.limpiar_campos()
        self.master.cambiar_frame(VentanaEjecutivoMesa)

    def limpiar_campos(self):
        self.entrada_nombre_cliente.delete(0, END)
        self.entrada_rut_cliente.delete(0, END)
        self.entrada_telefono_cliente.delete(0, END)
        self.entrada_email_cliente.delete(0, END)
        self.entrada_criticidad.delete(0, END)
        self.entrada_detalle_servicio.delete(0, END)
        self.entrada_detalle_problema.delete(0, END)
        self.entrada_ejecutivo_apertura.delete(0, END)
        self.entrada_fecha_apertura.delete(0, END)
        self.entrada_fecha_cierre.delete(0, END)
        self.entrada_ejecutivo_cierre.delete(0, END)


class Aplicacion(Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación de escritorio")
        self.geometry("700x700")
        self.cambiar_frame(VentanaInicioSesion)

    def cambiar_frame(self, clase_frame):
        nuevo_frame = clase_frame(self)
        if hasattr(self, "frame_actual"):
            self.frame_actual.destroy()
        self.frame_actual = nuevo_frame
        self.frame_actual.pack()


app = Aplicacion()
app.mainloop()
