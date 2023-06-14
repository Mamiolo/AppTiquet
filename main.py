from tkinter import *
from tkinter.ttk import Combobox  # Agrega esta línea
from tkinter import messagebox


class LoginWindow(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Inicio de sesión")
        self.username_label = Label(self, text="Usuario:")
        self.username_entry = Entry(self)
        self.password_label = Label(self, text="Contraseña:")
        self.password_entry = Entry(self, show="*")
        self.login_button = Button(self, text="Iniciar sesión", command=self.login)
        
        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.login_button.pack()
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Verificar las credenciales (aquí debes implementar tu lógica de autenticación)
        if username == "mesa" and password == "1234":
            self.master.switch_frame(EjecutivoMesa)
        else:
            messagebox.showerror("Error de inicio de sesión", "Credenciales incorrectas")



class EjecutivoMesa(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Interfaz Ejecutivo Mesa")

        self.crear_tiquet_button = Button(self, text="Crear Tiquet", command=self.crear_Tiquet)
        self.logout_button = Button(self, text="Cerrar sesión", command=self.logout)

        self.crear_tiquet_button.grid(row=10, column=0, pady=10)
        self.logout_button.grid(row=10, column=1, pady=10)


    def crear_Tiquet(self):
        self.master.switch_frame(TicketCreationWindow)

    def logout(self):
        self.master.switch_frame(LoginWindow)

class TicketCreationWindow(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Crear Tiquet")
        
        # Campos de tiquet
        self.client_name_label = Label(self, text="Nombre del cliente:")
        self.client_name_entry = Entry(self)
        self.client_rut_label = Label(self, text="RUT del cliente:")
        self.client_rut_entry = Entry(self)
        self.client_contact_label = Label(self, text="Datos de contacto del cliente:")
        self.client_phone_label = Label(self, text="Teléfono:")
        self.client_phone_entry = Entry(self)
        self.client_email_label = Label(self, text="Correo electrónico:")
        self.client_email_entry = Entry(self)
        self.ticket_type_label = Label(self, text="Tipo de tiquet:")
        self.ticket_type_var = StringVar()
        self.ticket_type_combobox = Combobox(self, textvariable=self.ticket_type_var, values=["Felicitación", "Consulta", "Reclamo", "Problema"])
        self.criticality_label = Label(self, text="Criticidad:")
        self.criticality_entry = Entry(self)
        self.service_detail_label = Label(self, text="Detalle del servicio:")
        self.service_detail_entry = Entry(self)
        self.problem_detail_label = Label(self, text="Detalle del problema:")
        self.problem_detail_entry = Entry(self)
        self.derive_area_label = Label(self, text="Área para derivar:")
        self.derive_area_var = StringVar()
        self.derive_area_combobox = Combobox(self, textvariable=self.derive_area_var, values=["Área 1", "Área 2", "Área 3", "No deriva"])
        self.executive_label = Label(self, text="Ejecutivo que abre el tiquet:")
        self.executive_entry = Entry(self)
        self.status_label = Label(self, text="Estado:")
        self.status_var = StringVar()
        self.status_combobox = Combobox(self, textvariable=self.status_var, values=["A resolución", "Resuelto", "No aplicable"])
        
        self.create_ticket_button = Button(self, text="Crear Tiquet", command=self.create_ticket)
        
        # Colocar los widgets en la ventana
        self.client_name_label.grid(row=0, column=0, sticky=W)
        self.client_name_entry.grid(row=0, column=1)
        self.client_rut_label.grid(row=1, column=0, sticky=W)
        self.client_rut_entry.grid(row=1, column=1)
        self.client_contact_label.grid(row=2, column=0, sticky=W)
        self.client_phone_label.grid(row=2, column=0, sticky=W)
        self.client_phone_entry.grid(row=2, column=1)
        self.client_email_label.grid(row=2, column=2, sticky=W)
        self.client_email_entry.grid(row=2, column=3)
        self.ticket_type_label.grid(row=3, column=0, sticky=W)
        self.ticket_type_combobox.grid(row=3, column=1)
        self.criticality_label.grid(row=4, column=0, sticky=W)
        self.criticality_entry.grid(row=4, column=1)
        self.service_detail_label.grid(row=5, column=0, sticky=W)
        self.service_detail_entry.grid(row=5, column=1)
        self.problem_detail_label.grid(row=6, column=0, sticky=W)
        self.problem_detail_entry.grid(row=6, column=1)
        self.derive_area_label.grid(row=7, column=0, sticky=W)
        self.derive_area_combobox.grid(row=7, column=1)
        self.executive_label.grid(row=8, column=0, sticky=W)
        self.executive_entry.grid(row=8, column=1)
        self.status_label.grid(row=9, column=0, sticky=W)
        self.status_combobox.grid(row=9, column=1)
        self.create_ticket_button.grid(row=10, column=0, pady=10)
        
    def create_ticket(self):
        # Obtener los valores ingresados por el usuario
        client_name = self.client_name_entry.get()
        client_rut = self.client_rut_entry.get()
        client_phone = self.client_phone_entry.get()
        client_email = self.client_email_entry.get()
        ticket_type = self.ticket_type_var.get()
        criticality = self.criticality_entry.get()
        service_detail = self.service_detail_entry.get()
        problem_detail = self.problem_detail_entry.get()
        derive_area = self.derive_area_var.get()
        executive = self.executive_entry.get()
        status = self.status_var.get()
        
        # Aquí debes implementar la lógica para guardar el tiquet en la base de datos
        # y generar un idTiquet único
        
        # Mostrar un mensaje de éxito y limpiar los campos
        messagebox.showinfo("Tiquet creado", "El tiquet se ha creado correctamente")
        self.clear_fields()
        self.master.switch_frame(EjecutivoMesa)
        
    def clear_fields(self):
        self.client_name_entry.delete(0, END)
        self.client_rut_entry.delete(0, END)
        self.client_phone_entry.delete(0, END)
        self.client_email_entry.delete(0, END)
        self.criticality_entry.delete(0, END)
        self.service_detail_entry.delete(0, END)
        self.problem_detail_entry.delete(0, END)
        self.executive_entry.delete(0, END)
        

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación de escritorio")
        self.geometry("700x700")
        self.switch_frame(LoginWindow)
        
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if hasattr(self, "current_frame"):
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack()

        
app = App()
app.mainloop()
