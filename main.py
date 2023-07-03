import mysql.connector
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from datetime import datetime
import re

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
        self.admin()

        self.etiqueta_usuario.pack()
        self.entrada_usuario.pack()
        self.etiqueta_contrasena.pack()
        self.entrada_contrasena.pack()
        self.boton_inicio_sesion.pack()

    def iniciar_sesion(self):
        usuario = self.entrada_usuario.get()
        contrasena = self.entrada_contrasena.get()
        self.master.user(usuario)

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="consultenos"
            )
        except mysql.connector.Error as error:
            messagebox.showerror("Error de conexión", str(error))
            return

        cursor = conexion.cursor()

        # Verificar las credenciales en la base de datos
        consulta = "SELECT rol FROM usuarios WHERE nombre_usuario = %s AND contraseña = %s"
        valores = (usuario, contrasena)
        cursor.execute(consulta, valores)
        resultado = cursor.fetchone()

        consulta = "SELECT nombre_area FROM usuarios WHERE nombre_usuario = %s AND contraseña = %s"
        valores = (usuario, contrasena)
        cursor.execute(consulta, valores)
        area = cursor.fetchone()


        if resultado is not None:
            rol = resultado[0]
            # cambiar el nombre del rol para que coincida con el frame que debe ingresar
            if rol == "jefe":
                self.master.cambiar_frame(VentanaJefeMesa)
            elif rol == "mesa":
                self.master.cambiar_frame(VentanaEjecutivoMesa)
            elif rol == "area":
                self.master.cambiar_frame(VentanaEjecutivoArea)
                self.master.areas(area[0])
            else:
                messagebox.showerror("Error de inicio de sesión", "No tienes permisos para acceder a esta interfaz")
        else:
            messagebox.showerror("Error de inicio de sesión", "Credenciales incorrectas")

        cursor.close()
        conexion.close()

    def admin(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="consultenos"
            )
        except mysql.connector.Error as error:
            messagebox.showerror("Error de conexión", str(error))
            return

        cursor = conexion.cursor()

        # Verificar si el usuario 'jefe' ya está creado
        consulta = "SELECT * FROM usuarios WHERE nombre_usuario = 'jefe'"
        cursor.execute(consulta)
        resultado = cursor.fetchone()

        if resultado is not None:
            None
        else:
            # Crear el usuario 'jefe'
            consulta = "INSERT INTO usuarios (nombre_usuario, contraseña, rol) VALUES (%s, %s, %s)"
            valores = ("jefe", "1234", "jefe")
            cursor.execute(consulta, valores)
            conexion.commit()

        cursor.close()
        conexion.close()


class VentanaEjecutivoMesa(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Interfaz Ejecutivo Mesa")

        self.boton_crear_tiquet = Button(self, text="Crear Tiquet", command=self.crear_tiquet)
        self.boton_cerrar_sesion = Button(self, text="Cerrar sesión", command=self.cerrar_sesion)

        self.boton_crear_tiquet.grid(row=10, column=0, pady=10)
        self.boton_cerrar_sesion.grid(row=10, column=2, pady=10)

    def crear_tiquet(self):
        self.master.cambiar_frame(VentanaCreacionTiquet)



    def cerrar_sesion(self):
        self.master.cambiar_frame(VentanaInicioSesion)




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
        self.combo_area_derivacion = Combobox(self)
        self.combo_area_derivacion.config(state="readonly")
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
        self.entrada_nombre_cliente.grid(row=1, column=0)
        self.etiqueta_rut_cliente.grid(row=2, column=0, sticky=W)
        self.entrada_rut_cliente.grid(row=3, column=0)
        self.etiqueta_telefono_cliente.grid(row=5, column=0, sticky=W)
        self.entrada_telefono_cliente.grid(row=6, column=0)
        self.etiqueta_email_cliente.grid(row=7, column=0, sticky=W)
        self.entrada_email_cliente.grid(row=8, column=0)
        self.etiqueta_tipo_tiquet.grid(row=9, column=0, sticky=W)
        self.combobox_tipo_tiquet.grid(row=10, column=0)
        self.etiqueta_criticidad.grid(row=11, column=0, sticky=W)
        self.entrada_criticidad.grid(row=12, column=0)
        self.etiqueta_detalle_servicio.grid(row=13, column=0, sticky=W)
        self.entrada_detalle_servicio.grid(row=14, column=0)
        self.etiqueta_detalle_problema.grid(row=15, column=0, sticky=W)
        self.entrada_detalle_problema.grid(row=16, column=0)
        self.etiqueta_area_derivacion.grid(row=17, column=0, sticky=W)
        self.combo_area_derivacion.grid(row=18, column=0)
        self.etiqueta_ejecutivo_apertura.grid(row=19, column=0, sticky=W)
        self.entrada_ejecutivo_apertura.grid(row=20, column=0)
        self.etiqueta_estado.grid(row=21, column=0, sticky=W)
        self.combobox_estado.grid(row=22, column=0)
        self.etiqueta_fecha_apertura.grid(row=23, column=0, sticky=W)
        self.entrada_fecha_apertura.grid(row=24, column=0)
        self.etiqueta_fecha_cierre.grid(row=25, column=0, sticky=W)
        self.entrada_fecha_cierre.grid(row=26, column=0)
        self.etiqueta_ejecutivo_cierre.grid(row=27, column=0, sticky=W)
        self.entrada_ejecutivo_cierre.grid(row=28, column=0)
        self.boton_crear_tiquet.grid(row=29, column=0, pady=10)

        



        self.cargar_areas()
        self.cargar_nombre()



    def cargar_areas(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="consultenos"
            )
        except mysql.connector.Error as error:
            messagebox.showerror("Error de conexión", str(error))
            return

        cursor = conexion.cursor()

        # Obtener las áreas desde la base de datos
        consulta = "SELECT nombre_area FROM areas"
        cursor.execute(consulta)
        areas = cursor.fetchall()

        # Actualizar los valores del combobox
        self.combo_area_derivacion["values"] = [area[0] for area in areas]

        cursor.close()
        conexion.close()

    def cargar_nombre(self):
        nombre = self.master.nombre
        self.entrada_ejecutivo_apertura.insert(0, nombre)
        self.entrada_ejecutivo_apertura.config(state="readonly")


    def crear_tiquet(self):

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
        area_derivacion = self.combo_area_derivacion.get()
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

        #ingresa las campos a la base de datos
        cursor = conexion.cursor()
        consulta = "INSERT INTO tiquets (nombre_cliente, rut_cliente, telefono_cliente, email_cliente, tipo_tiquet, criticidad, detalle_servicio, detalle_problema, nombre_area, ejecutivo_apertura, estado, fecha_apertura, fecha_cierre, ejecutivo_cierre) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (nombre_cliente, rut_cliente, telefono_cliente, email_cliente, tipo_tiquet, criticidad, detalle_servicio, detalle_problema, area_derivacion, ejecutivo_apertura, estado, fecha_apertura, fecha_cierre, ejecutivo_cierre)
        print(area_derivacion)
        cursor.execute(consulta, valores)
        conexion.commit()
        cursor.close()
        conexion.close()

        messagebox.showinfo("Tiquet creado", "El tiquet se ha creado correctamente")
        self.limpiar_campos()
        self.master.cambiar_frame(VentanaEjecutivoMesa)

    def limpiar_campos(self):
        #limpia los campos
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

class VentanaJefeMesa(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Interfaz Jefe de Mesa")

        self.boton_usuarios = Button(self, text="Usuarios", command=self.mostrar_ventana_usuarios)
        self.boton_areas = Button(self, text="Areas", command=self.mostrar_ventana_areas)
        self.boton_tiquets = Button(self, text="Tiquets", command=self.mostrar_ventana_tiquets)

        self.boton_cerrar_sesion = Button(self, text="Cerrar sesión", command=self.cerrar_sesion)



        
        self.boton_usuarios.pack()
        self.boton_tiquets.pack()
        self.boton_areas.pack()
        self.boton_cerrar_sesion.pack()

    def mostrar_ventana_usuarios(self):
        self.master.cambiar_frame(JefeMesaUsuarios)

    def mostrar_ventana_tiquets(self):
        self.master.cambiar_frame(VentanaTiquets)

    def mostrar_ventana_areas(self):
        self.master.cambiar_frame(VentanaAreas)
    
    def cerrar_sesion(self):
        self.master.cambiar_frame(VentanaInicioSesion)

class JefeMesaUsuarios(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Gestión de Usuarios - Jefe de Mesa")

        self.boton_crear_usuario = Button(self, text="Crear usuario", command=self.crear_usuario)
        self.boton_eliminar_usuario = Button(self, text="Eliminar usuario", command=self.eliminar_usuario)
        self.boton_volver = Button(self, text="Volver", command=self.volver)

        self.boton_crear_usuario.pack()
        self.boton_eliminar_usuario.pack()
        self.boton_volver.pack()

    def crear_usuario(self):
        self.master.cambiar_frame(VentanaRegistro)

    def eliminar_usuario(self):
        self.master.cambiar_frame(EliminarUsuario)

    def volver(self):
        self.master.cambiar_frame(VentanaJefeMesa)

class VentanaRegistro(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Registro de usuario")

        self.etiqueta_nombre = Label(self, text="Nombre de usuario:")
        self.entrada_nombre = Entry(self)
        self.etiqueta_contrasena = Label(self, text="Contraseña:")
        self.entrada_contrasena = Entry(self, show="*")
        self.etiqueta_rol = Label(self, text="Rol:")
        self.entrada_rol = Entry(self)
        self.etiqueta_area = Label(self, text="Seleccione el área a eliminar:")
        self.combo_area = Combobox(self)
        self.boton_registrar = Button(self, text="Registrar", command=self.registrar_usuario)

        self.etiqueta_nombre.pack()
        self.entrada_nombre.pack()
        self.etiqueta_contrasena.pack()
        self.entrada_contrasena.pack()
        self.etiqueta_rol.pack()
        self.entrada_rol.pack()
        self.etiqueta_area.pack()
        self.combo_area.pack()
        self.boton_registrar.pack()


        self.cargar_areas()

    def cargar_areas(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="consultenos"
            )
        except mysql.connector.Error as error:
            messagebox.showerror("Error de conexión", str(error))
            return

        cursor = conexion.cursor()


        consulta = "SELECT nombre_area FROM areas"
        cursor.execute(consulta)
        resultados = cursor.fetchall()

        areas = [resultado[0] for resultado in resultados]

        # Cargar las áreas en el combo box para seleccionarla
        self.combo_area['values'] = areas

        cursor.close()
        conexion.close()

    def registrar_usuario(self):
        nombre = self.entrada_nombre.get()
        contraseña = self.entrada_contrasena.get()
        rol = self.entrada_rol.get()
        area_seleccionada = self.combo_area.get()

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="consultenos"
            )
        except mysql.connector.Error as error:
            messagebox.showerror("Error de conexión", str(error))
            return

        cursor = conexion.cursor()

        # Insertar el nuevo usuario en la tabla usuarios
        try:
            consulta = "INSERT INTO usuarios (nombre_usuario, contraseña, rol, nombre_area) VALUES (%s, %s, %s, %s)"
            valores = (nombre, contraseña, rol, area_seleccionada)
            print(area_seleccionada)
            cursor.execute(consulta, valores)
            conexion.commit()
        except mysql.connector.Error as error:
            messagebox.showerror("Error al registrar usuario", str(error))
            conexion.rollback()
        else:
            messagebox.showinfo("Registro exitoso", "El usuario se ha registrado correctamente")
            self.master.cambiar_frame(JefeMesaUsuarios)

        cursor.close()
        conexion.close()

class EliminarUsuario(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Eliminar Usuario")

        self.lista_usuarios = Listbox(self, height=10)
        self.boton_eliminar = Button(self, text="Eliminar", command=self.eliminar_usuario)
        self.boton_volver = Button(self, text="Volver", command=self.volver)

        self.cargar_usuarios()

        self.lista_usuarios.pack()
        self.boton_eliminar.pack()
        self.boton_volver.pack()

    def cargar_usuarios(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="consultenos"
            )
        except mysql.connector.Error as error:
            messagebox.showerror("Error de conexión", str(error))
            return

        cursor = conexion.cursor()
        consulta = "SELECT nombre_usuario FROM usuarios"
        cursor.execute(consulta)
        usuarios = cursor.fetchall()

        for usuario in usuarios:
            self.lista_usuarios.insert(END, usuario[0])

        cursor.close()
        conexion.close()

    def eliminar_usuario(self):
        seleccionado = self.lista_usuarios.curselection()

        if seleccionado:
            usuario = self.lista_usuarios.get(seleccionado)

            if usuario == "jefe":
                messagebox.showwarning("Eliminar Usuario", "No se puede eliminar al usuario 'jefe'")
                return

            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="consultenos"
                )
            except mysql.connector.Error as error:
                messagebox.showerror("Error de conexión", str(error))
                return

            cursor = conexion.cursor()

            # Eliminar el usuario de la base de datos
            consulta = "DELETE FROM usuarios WHERE nombre_usuario = %s"
            valores = (usuario,)
            cursor.execute(consulta, valores)
            conexion.commit()

            messagebox.showinfo("Eliminar Usuario", f"Usuario '{usuario}' eliminado correctamente")

            cursor.close()
            conexion.close()

            self.lista_usuarios.delete(seleccionado)
        else:
            messagebox.showwarning("Eliminar Usuario", "Seleccione un usuario de la lista")

    def volver(self):
        self.master.cambiar_frame(VentanaJefeMesa)


class VentanaTiquets(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Tiquets")

        self.lista_tiquets = Listbox(self, height=25, width=100)
        self.boton_volver = Button(self, text="Volver", command=self.volver)

        self.cargar_tiquets()  

        self.lista_tiquets.pack()
        self.boton_volver.pack()

    def cargar_tiquets(self):

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
            self.lista_tiquets.insert(END, tiquet)  

    def volver(self):
        self.master.cambiar_frame(VentanaEjecutivoMesa)


class VentanaAreas(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Áreas")

        self.boton_crear_areas = Button(self, text="Crear áreas", command=self.crear_areas)
        self.boton_crear_areas.pack()

        self.boton_eliminar_areas = Button(self, text="Eliminar áreas", command=self.eliminar_areas)
        self.boton_eliminar_areas.pack()

    def crear_areas(self):
        self.master.cambiar_frame(VentanaCrearArea)


    def eliminar_areas(self):
        self.master.cambiar_frame(VentanaEliminarArea)



class VentanaCrearArea(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Áreas")

        self.etiqueta_nombre = Label(self, text="Nombre del área:")
        self.entrada_nombre = Entry(self)
        self.boton_crear = Button(self, text="Crear", command=self.crear_area)

        self.etiqueta_nombre.pack()
        self.entrada_nombre.pack()
        self.boton_crear.pack()

    def crear_area(self):
        nombre_area = self.entrada_nombre.get()

        if not nombre_area:
            messagebox.showerror("Error", "Debes ingresar un nombre para el área.")
            return

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="consultenos"
            )
        except mysql.connector.Error as error:
            messagebox.showerror("Error de conexión", str(error))
            return

        cursor = conexion.cursor()

        # Verificar si el área ya existe
        consulta = "SELECT * FROM areas WHERE nombre_area = %s"
        valores = (nombre_area,)
        cursor.execute(consulta, valores)
        resultado = cursor.fetchone()

        if resultado is not None:
            messagebox.showerror("Error", "El área ya existe.")
            return

        # Crear el área
        consulta = "INSERT INTO areas (nombre_area) VALUES (%s)"
        valores = (nombre_area,)
        cursor.execute(consulta, valores)
        conexion.commit()

        messagebox.showinfo("Éxito", "Área creada exitosamente.")

        cursor.close()
        conexion.close()



class VentanaEliminarArea(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Áreas")

        self.etiqueta_area = Label(self, text="Seleccione el área a eliminar:")
        self.combo_area = Combobox(self)
        self.boton_eliminar = Button(self, text="Eliminar", command=self.eliminar_area)

        self.etiqueta_area.pack()
        self.combo_area.pack()
        self.boton_eliminar.pack()

        self.cargar_areas()

    def cargar_areas(self):
        
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="consultenos"
            )
        except mysql.connector.Error as error:
            messagebox.showerror("Error de conexión", str(error))
            return

        cursor = conexion.cursor()

        consulta = "SELECT nombre_area FROM areas"
        cursor.execute(consulta)
        resultados = cursor.fetchall()

        areas = [resultado[0] for resultado in resultados]

        # Cargar las áreas en el combo box
        self.combo_area['values'] = areas

        cursor.close()
        conexion.close()

    def eliminar_area(self):
        area_seleccionada = self.combo_area.get()

        if not area_seleccionada:
            messagebox.showerror("Error", "Debes seleccionar un área.")
            return

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="consultenos"
            )
        except mysql.connector.Error as error:
            messagebox.showerror("Error de conexión", str(error))
            return

        cursor = conexion.cursor()

        # Eliminar el área
        consulta = "DELETE FROM areas WHERE nombre_area = %s"
        valores = (area_seleccionada,)
        cursor.execute(consulta, valores)
        conexion.commit()

        messagebox.showinfo("Éxito", "Área eliminada exitosamente.")

        cursor.close()
        conexion.close()







class VentanaEjecutivoArea(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Interfaz Área")

        self.lista_tiquets = Listbox(self, height=25, width=100)
        self.boton_cargar = Button(self, text="Cargar Tiquets", command=self.cargar_tiquets)
        self.boton_volver = Button(self, text="Cerrar Sesión", command=self.cerrar_sesion)

        self.lista_tiquets.pack()
        self.boton_cargar.pack()
        self.boton_volver.pack()

    def cargar_tiquets(self):
        area = self.master.area
        print(area)


        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="consultenos"
        )
        cursor = conexion.cursor()
        consulta = "SELECT * FROM tiquets WHERE nombre_area = %s"
        valores = (str(area),)
        cursor.execute(consulta, valores)
        tiquets = cursor.fetchall()
        conexion.close()
        print(area)

        if len(tiquets) == 0:
            messagebox.showinfo("Sin tiquets", "No hay tiquets para mostrar.")
        else:
            for tiquet in tiquets:
                self.lista_tiquets.insert(END, tiquet)


        self.boton_cargar.config(state="disable")


    def cerrar_sesion(self):
        self.master.cambiar_frame(VentanaInicioSesion)




class Aplicacion(Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación de escritorio")
        self.geometry("1000x1000")
        self.cambiar_frame(VentanaInicioSesion)

    def cambiar_frame(self, clase_frame):
        nuevo_frame = clase_frame(self)
        if hasattr(self, "frame_actual"):
            self.frame_actual.destroy()
        self.frame_actual = nuevo_frame
        self.frame_actual.pack()

    def user(self, nombre):
        self.nombre = nombre
        print(nombre)

    def areas(self, area):
        self.area = area
        print(area)
        

app = Aplicacion()
app.mainloop()
