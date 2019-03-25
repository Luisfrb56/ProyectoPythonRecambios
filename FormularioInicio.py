import gi
import sqlite3
import InformeClientes
import InformeFactura
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

#Creamos la clase inicial para iniciar las siguientes.
class FormularioInicio(Gtk.Window):

    def __init__(self):
        #Creamos la ventana con un tamaño y un borde para el resto de widgets.
        Gtk.Window.__init__(self, title="Formulario Inicial")
        self.set_default_size(400,50)
        self.set_border_width(10)
        #Creamos la caja donde colocamos todos los widgets.
        cajaExterior = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
        self.add(cajaExterior)

        #Creamos el frame para cada apartado.
        frame = Gtk.Frame()
        frame.set_shadow_type(1)

        #Creamos un grid para meter todas las operaciones que queramos.
        grid=Gtk.Grid()
        cajaExterior.add(grid)
        #Label de la seleccion de formularios
        lblFormularios=Gtk.Label("Selecciona un formulario:",xalign=0.1)
        #Una array para luego llenar el comboBox
        grid.add(lblFormularios)
        formularios=["Gestión Clientes", "Gestión Productos/Servicios"]

        cmbFormularios=Gtk.ComboBoxText()
        cmbFormularios.set_entry_text_column(0)
        #Con este for recorremos el array y llenamos el combo
        for formulario in formularios:
            cmbFormularios.append_text(formulario)
        cmbFormularios.connect("changed", self.on_formulario_changed)
        #Lo metemos dentro de grid con attach para dat la posicion.
        grid.attach_next_to(cmbFormularios,lblFormularios,Gtk.PositionType.RIGHT, 1,1)


        #Boton salir que cerrara la aplicacion.
        botonSalida=Gtk.Button.new_with_label("Salir")
        botonSalida.connect('clicked', self.on_click_salida)
        cajaExterior.add(botonSalida)

        #Mostramos la clase entera y siguientes.
        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    #Evento del boton salir que al clicar cierre la app.
    def on_click_salida(self, botonSalida):
        """
        Cierra la aplicacion.
        :param botonSalida:
        :return: nothing
        """
        print("Saliendo...")
        Gtk.main_quit()

    #Evento de la selecion del formulario para que dependiendo del selecionado se abra.
    def on_formulario_changed(self,combo):
        """
        Abre el formulario que tengas selecionado.
        :param combo:
        :return: nothing
        """
        text=combo.get_active_text()
        #Creamos dos variables para luego comparar cual es cual.
        opcion1="Gestión Clientes"
        opcion2="Gestión Productos/Servicios"
        #Un if para saber si es la opcion uno, es decir, gestion clientes o gestion servicios.
        if text == opcion1:
        #Aqui dentro llamamos a la clase que corresponda.
            cli=GestionCliente()
            cli.show_all()
        elif text==opcion2:
            serv=GestionServProd()
            serv.show_all()

#Clase gestion cliente.
class GestionCliente(Gtk.Window):
    def __init__(self):
        #Ventana con el nombre Clientes y damos tamaño y borde ademas de la caja donde incluiremos todo.
        Gtk.Window.__init__(self, title="Clientes")
        self.set_default_size(600, 200)
        self.set_border_width(10)
        cajaExterior2=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
        self.add(cajaExterior2)
        #Creamos dos frames, uno para insertar clientes nuevos y otro para borrar.
        frameInsertar=Gtk.Frame()
        frameInsertar.set_label("Registro Cliente")

        frameBorrar=Gtk.Frame()
        frameBorrar.set_label("Borrar Cliente")
        #Los guardamos dentro de la caja exterior y creamos 2 grids para incluirlos en los frames respectivamente.
        cajaExterior2.add(frameInsertar)
        cajaExterior2.add(frameBorrar)
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)

        self.grid2=Gtk.Grid()
        self.grid2.set_column_spacing(10)

        frameInsertar.add(grid)

        self.grid3=Gtk.Grid()
        self.grid3.set_column_spacing(10)
        self.grid3.set_row_spacing(10)
        frameBorrar.add(self.grid3)

        #Creamos un boton ver tabla que servira exactamente para eso, luego veremos el evento.
        verTabla=Gtk.Button(label='Consultar Clientes')
        verTabla.connect("clicked", self.on_listar_clicked)

        #Declaramos los labels y sus entrys que se incluiran en el grid con attach para poner cada uno a la altura correspondiente
        self.lblDNI=Gtk.Label("DNI: ")
        self.txtDNI=Gtk.Entry()
        self.lblNombre=Gtk.Label("Nombre: ")
        self.txtNombre=Gtk.Entry()
        self.lblApellido=Gtk.Label("Apellido: ")
        self.txtApellido=Gtk.Entry()
        self.lblMatricula=Gtk.Label("Matricula: ")
        self.txtMatricula=Gtk.Entry()
        self.lblAutomovil=Gtk.Label("Automovil: ")
        #Creamos tambien un radioButton para elegir una de las tres opciones correspondientes.
        self.botonCoche=Gtk.RadioButton(label="Coche")
        self.botonMoto=Gtk.RadioButton.new_from_widget(self.botonCoche)
        self.botonMoto.set_label("Moto")
        self.botonMoto.set_active(False)
        self.botonCamion=Gtk.RadioButton.new_from_widget(self.botonCoche)
        self.botonCamion.set_label("Camion")
        self.botonCamion.set_active(False)
        self.lblMarca=Gtk.Label("Marca: ")
        self.txtMarca=Gtk.Entry()
        self.lblTelefono=Gtk.Label("Telefono: ")
        self.txtTelefono=Gtk.Entry()
        self.lblAñoMatri=Gtk.Label("Año de Matriculacion: ")
        self.txtAñoMatri=Gtk.Entry()

        #Tambien metemos el boton insertar que recogera todos los datos que hemos introducido
        self.insertar=Gtk.Button(label='Insertar Cliente')
        self.insertar.connect("clicked", self.on_insertar_clicked)

        #Este es el apartado de borrar clientes, donde lo haremos por su dni.
        self.lblBorrar=Gtk.Label("DNI: ")
        #tenemos un combobox que llenamos con los dni que hay para no tener que meterlo a mano.
        self.cbDNI=Gtk.ComboBoxText()
        self.cbDNI.set_entry_text_column(0)
        #Llamada a un evento para listar los dni
        self.dni_cliente()
        self.borrar=Gtk.Button(label='Borrar Cliente')
        self.borrar.connect("clicked",self.on_borrar_clicked)
        #El grid2 metemos los radiobuttons que luego meteremos en el grid1
        self.grid2.attach(self.botonCoche, 0,0,1,1)
        self.grid2.attach(self.botonMoto, 1,0,1,1)
        self.grid2.attach(self.botonCamion,2,0,1,1)

        self.grid3.attach(self.lblBorrar,0,0,1,1)
        self.grid3.attach(self.cbDNI,1,0,1,1)
        self.grid3.attach(self.borrar,2,1,1,1)

        grid.attach(self.lblDNI,0,0,1,1)
        grid.attach(self.txtDNI,1,0,1,1)
        grid.attach(self.lblMatricula,2,0,1,1)
        grid.attach(self.txtMatricula,3,0,1,1)
        grid.attach(self.lblNombre,0,1,1,1)
        grid.attach(self.txtNombre, 1, 1, 1, 1)
        grid.attach(self.lblApellido, 2, 1, 1, 1)
        grid.attach(self.txtApellido, 3, 1, 1, 1)
        grid.attach(self.lblAutomovil,0,2,1,1)
        grid.attach(self.grid2,1,2,1,1)
        grid.attach(self.lblMarca,2,2,1,1)
        grid.attach(self.txtMarca,3,2,1,1)
        grid.attach(self.lblTelefono,0,3,1,1)
        grid.attach(self.txtTelefono,1,3,1,1)
        grid.attach(self.lblAñoMatri,2,3,1,1)
        grid.attach(self.txtAñoMatri,3,3,1,1)

        grid.attach(self.insertar,0,4,2,1)


        cajaExterior2.add(verTabla)

    #Evento que lista los dni y llena el combobox.
    def dni_cliente(self):
        """
        Lista los clientes en el combobox.
        :return: nothing
        """
        #Este codigo lo utilizo para cuando se borre algun cliente poder actulizar los dni
        self.cbDNI.remove_all()
        #Conectamos a la base con sqlite3 connect y guardamos en un cursor que luego ejecutaremos un select.
        tiendaC=sqlite3.connect("BaseTiendaRecambios.dat")
        cursor=tiendaC.cursor()
        try:

            cursor.execute("select DNI from Clientes")
            for rexistro in cursor.fetchall():
                self.cbDNI.append_text(rexistro[0])
        finally:
            cursor.close()
            tiendaC.close()

    #Evento que inserta todos los datos, guarda cada dato de los entry en una variable que luego seran introducidos en la base.
    def on_insertar_clicked(self,btn):
        """
        Recoge en unas variables los entrys y los inserta en la base de datos.
        :param btn:
        :return: nothing
        """
        DNI=self.txtDNI.get_text()
        Nombre=self.txtNombre.get_text()
        Apellido=self.txtApellido.get_text()
        Matricula=self.txtMatricula.get_text()
        Marca=self.txtMarca.get_text()
        Telefono=self.txtTelefono.get_text()
        AñoMatri=self.txtAñoMatri.get_text()

    #Un if para saber que radiobutton esta selecionado y guardamos en una variable respectivamente.
        if self.botonCoche.get_active():
            automovil="Coche"
        elif self.botonMoto.get_active():
            automovil="Moto"
        elif self.botonCamion.get_active():
            automovil="Camion"

    #
        self.txtDNI.set_text("")
        self.txtNombre.set_text("")
        self.txtApellido.set_text("")
        self.txtMarca.set_text("")
        self.txtMatricula.set_text("")
        self.txtTelefono.set_text("")
        self.txtAñoMatri.set_text("")


        tienda=sqlite3.connect("BaseTiendaRecambios.dat")
        cursor=tienda.cursor()
        try:
            sql="INSERT INTO Clientes (DNI, Nombre, Apellido, Automovil, Marca, Telefono, Matricula, AñoMatricula) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            parametros=(DNI,Nombre,Apellido,automovil, Marca, Telefono, Matricula,AñoMatri)

            cursor.execute(sql, parametros)
            tienda.commit()
            print("Insercion completada con exito!")
            self.dni_cliente()
        finally:
            cursor.close()
            tienda.close()

    def on_borrar_clicked(self,btn2):
        """
        Borrar un cliente de una base de datos a traves del dni que seleciona en el combobox
        :param btn2:
        :return: nothing
        """
        DNI= self.cbDNI.get_active_text()
        tienda=sqlite3.connect("BaseTiendaRecambios.dat")
        cursor=tienda.cursor()
        try:
            sql="DELETE FROM Clientes WHERE DNI='"+DNI+"'"
            cursor.execute(sql)
            tienda.commit()
            print("Cliente con DNI: "+DNI+" ha sido eliminado")
            self.dni_cliente()
        finally:
            cursor.close()
            tienda.close()


    def on_listar_clicked(self,verTabla):
        """
        Visualiza la clase donde vamos hacer la consulta y ver la base.
        :param verTabla:
        :return: nothing
        """
        tbCli=TablaClientes()
        tbCli.show_all()



class TablaClientes(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Listado Clientes")
        self.set_default_size(400,300)

        self.set_border_width(10)

        self.grid=Gtk.Grid()
        self.grid.set_column_spacing(10)
        self.grid.set_row_spacing(10)

        self.cajaVentana = Gtk.Box(spacing=20)
        self.cajaVentana.set_orientation(Gtk.Orientation.VERTICAL)

        self.add(self.cajaVentana)
        self.cajaVentana.add(self.grid)

        self.lblDNI=Gtk.Label("DNI: ")
        self.lsDNI=Gtk.ComboBoxText()
        self.lsDNI.set_entry_text_column(0)
        self.btnConsultar=Gtk.Button("Consultar")
        self.btnConsultar.connect("clicked", self.on_consulta_clicked)
        self.btnMostrar=Gtk.Button("Mostrar Todos")
        self.btnMostrar.connect("clicked", self.on_mostrar_click)


        self.btnInforme=Gtk.Button("Crear Informe")
        self.btnInforme.connect("clicked", self.on_informe)
        self.grid.attach(self.lblDNI,0,0,1,1)
        self.grid.attach(self.lsDNI,1,0,1,1)
        self.grid.attach(self.btnConsultar,2,0,1,1)
        self.grid.attach(self.btnMostrar,3,0,1,1)
        self.grid.attach(self.btnInforme,5,0,1,1)
        self.dni_cliente()


        self.columnas = ["DNI", "Nombre", "Apellidos", "Automovil", "Marca", "Telefono", "Matricula", "Año Matriculacion"]
        self.modelo = Gtk.ListStore(str, str, str, str, str, str, str, str)



        self.axenda = []
        self.vista = Gtk.TreeView(model=self.modelo)

        for i in range(len(self.columnas)):
            celda = Gtk.CellRendererText()
            self.columna = Gtk.TreeViewColumn(self.columnas[i], celda, text=i)
            self.vista.append_column(self.columna)

        self.cajaVentana.add(self.vista)



    def on_informe(self,btnIn):
        tiendaRe=sqlite3.connect("BaseTiendaRecambios.dat")
        cursor=tiendaRe
        result= cursor.execute("select * from Clientes where dni='"+self.lsDNI.get_active_text()+"'")
        lista=[]
        for elemento in result:
            lista.append(elemento)
        cursor.close()
        InformeClientes.informeCliente(lista)


    def on_mostrar_click(self,btMostrar):
        """
        Muestra toda la tabla de la base de datos.
        :param btMostrar:
        :return: nothing
        """
        self.columnas.clear()
        tiendaC = sqlite3.connect("BaseTiendaRecambios.dat")
        cursor = tiendaC.cursor()
        try:
            cursor.execute("select * from Clientes")
            self.axenda.clear()
            for rexistro in cursor.fetchall():
                self.axenda.append(
                    [rexistro[0], rexistro[1], rexistro[2], rexistro[3], rexistro[4], rexistro[5], rexistro[6], rexistro[7]])
            self.modelo.clear()
            for elemento in self.axenda:
                self.modelo.append(elemento)




        finally:
            cursor.close()
            tiendaC.close()

    def on_consulta_clicked(self,btnConsu):

        """
        Gracias al dni visualizamos en cliente que queramos.
        :param btnConsu:
        :return: nothing
        """
        tiendaC = sqlite3.connect("BaseTiendaRecambios.dat")
        cursor = tiendaC.cursor()
        try:
            cursor.execute("select * from Clientes WHERE DNI='"+self.lsDNI.get_active_text()+"'")
            self.axenda.clear()

            for rexistro in cursor.fetchall():
                self.axenda.append(
                    [rexistro[0], rexistro[1], rexistro[2], rexistro[3], rexistro[4], rexistro[5], rexistro[6], rexistro[7]])
            self.modelo.clear()
            for elemento in self.axenda:
                self.modelo.append(elemento)


        finally:
            cursor.close()
            tiendaC.close()

    def dni_cliente(self):
        """
        Lista los clientes y los muestra en un combobox para realizar la consulta
        :return: nothing
        """
        tiendaC=sqlite3.connect("BaseTiendaRecambios.dat")
        cursor=tiendaC.cursor()
        try:

            cursor.execute("select DNI from Clientes")
            for rexistro in cursor.fetchall():
                self.lsDNI.append_text(rexistro[0])
        finally:
            cursor.close()
            tiendaC.close()



class GestionServProd(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Servicios/Productos")
        self.set_default_size(600, 200)
        self.set_border_width(10)

        cajaExterior2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(cajaExterior2)
        frameInsertar = Gtk.Frame()
        frameInsertar.set_label("Registro Producto")

        frameBorrar = Gtk.Frame()
        frameBorrar.set_label("Borrar Producto")

        cajaExterior2.add(frameInsertar)
        cajaExterior2.add(frameBorrar)
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)

        frameInsertar.add(grid)

        self.grid3 = Gtk.Grid()
        self.grid3.set_column_spacing(10)
        self.grid3.set_row_spacing(10)
        frameBorrar.add(self.grid3)


        verTabla = Gtk.Button(label='Listar Servicios')
        verTabla.connect("clicked", self.on_listar_clicked)

        self.lblID = Gtk.Label("ID: ")
        self.txtID = Gtk.Entry()
        self.lblMatricula= Gtk.Label("Matricula: ")
        self.cbMatri = Gtk.ComboBoxText()
        self.cbMatri.set_entry_text_column(0)
        self.lblNombre= Gtk.Label("Nombre: ")
        self.txtNombre = Gtk.Entry()
        self.lblPrecio= Gtk.Label("Precio: ")
        self.txtPrecio = Gtk.Entry()
        self.lblMarca = Gtk.Label("Marca: ")
        self.txtMarca = Gtk.Entry()
        self.lblProcedencia = Gtk.Label("Procedencia: ")
        self.txtProcedencia= Gtk.Entry()
        self.lblAñoFabri= Gtk.Label("Año de Fabricacion: ")
        self.txtAñoFabri = Gtk.Entry()

        self.insertar = Gtk.Button(label='Insertar Producto')
        self.insertar.connect("clicked", self.on_insertar_clicked)

        self.lblBorrar = Gtk.Label("ID: ")
        self.cbBId = Gtk.ComboBoxText()
        self.cbBId.set_entry_text_column(0)
        self.matri_cliente()
        self.id_producto()
        self.borrar = Gtk.Button(label='Borrar Producto')
        self.borrar.connect("clicked", self.on_borrar_clicked)

        self.grid3.attach(self.lblBorrar, 0, 0, 1, 1)
        self.grid3.attach(self.cbBId, 1, 0, 1, 1)
        self.grid3.attach(self.borrar, 2, 1, 1, 1)

        grid.attach(self.lblID, 0, 0, 1, 1)
        grid.attach(self.txtID, 1, 0, 1, 1)
        grid.attach(self.lblMatricula, 2, 0, 1, 1)
        grid.attach(self.cbMatri, 3, 0, 1, 1)
        grid.attach(self.lblNombre, 0, 1, 1, 1)
        grid.attach(self.txtNombre, 1, 1, 1, 1)
        grid.attach(self.lblPrecio, 2, 1, 1, 1)
        grid.attach(self.txtPrecio, 3, 1, 1, 1)
        grid.attach(self.lblMarca, 0, 2, 1, 1)
        grid.attach(self.txtMarca, 1, 2, 1, 1)
        grid.attach(self.lblProcedencia, 2, 2, 1, 1)
        grid.attach(self.txtProcedencia, 3, 2, 1, 1)
        grid.attach(self.lblAñoFabri, 0, 3, 1, 1)
        grid.attach(self.txtAñoFabri, 1, 3, 1, 1)

        grid.attach(self.insertar, 0, 4, 2, 1)

        cajaExterior2.add(verTabla)

    def matri_cliente(self):
        """
        Lista las matriculas y las mete en un combobox para que cada producto nuevo tenga que ser de un cliente registrado.
        :return: nothing
        """
        tiendaC = sqlite3.connect("BaseTiendaRecambios.dat")
        cursor = tiendaC.cursor()
        try:

            cursor.execute("select Matricula from Clientes")
            for rexistro in cursor.fetchall():
                self.cbMatri.append_text(rexistro[0])
        finally:
            cursor.close()
            tiendaC.close()
    def id_producto(self):

        """
        Lista los id de los productos y los guarda en un combobox para borrar el producto
        :return: nothing
        """
        self.cbBId.remove_all()
        tiendaC = sqlite3.connect("BaseTiendaRecambios.dat")
        cursor = tiendaC.cursor()
        try:

            cursor.execute("select IdProd from Productos")
            for rexistro in cursor.fetchall():
                self.cbBId.append_text(rexistro[0])
        finally:
            cursor.close()
            tiendaC.close()

    def on_insertar_clicked(self, btn):
        """
        Insertar producto, recoge todos los entry en variables para introducirlos en la base de datos
        :param btn:
        :return: nothing
        """
        ID = self.txtID.get_text()
        Matricula=self.cbMatri.get_active_text()
        Nombre = self.txtNombre.get_text()
        Precio = self.txtPrecio.get_text()
        Marca = self.txtMarca.get_text()
        Procedencia = self.txtProcedencia.get_text()
        AñoFabr = self.txtAñoFabri.get_text()

        self.txtID.set_text("")
        self.txtNombre.set_text("")
        self.txtPrecio.set_text("")
        self.txtMarca.set_text("")
        self.txtProcedencia.set_text("")
        self.txtAñoFabri.set_text("")


        tienda = sqlite3.connect("BaseTiendaRecambios.dat")
        cursor = tienda.cursor()
        try:
            sql = "INSERT INTO Productos (IdProd, Matriculas, Nombre, Precio, Marca, Procedencia, AñoFabricacion) VALUES (?, ?, ?, ?, ?, ?, ?)"
            parametros = (ID, Matricula, Nombre, Precio, Marca, Procedencia, AñoFabr)

            cursor.execute(sql, parametros)
            tienda.commit()
            print("Insercion completada con exito!")
            self.id_producto()
        finally:
            cursor.close()
            tienda.close()

    def on_borrar_clicked(self, btn2):
        """
        Borrar producto a traves del combobox que contiene el id.
        :param btn2:
        :return: nothing
        """
        ID = self.cbBId.get_active_text()
        tienda = sqlite3.connect("BaseTiendaRecambios.dat")
        cursor = tienda.cursor()
        try:
            sql = "DELETE FROM Productos WHERE IdProd='" + ID + "'"
            cursor.execute(sql)
            tienda.commit()
            print("Producto con ID: " + ID + " ha sido eliminado")
            self.id_producto()
        finally:
            cursor.close()
            tienda.close()







    def on_listar_clicked(self,verTabla):
        """
        Lista la tabla servicios para poder consultar y motrar.
        :param verTabla:
        :return: nothing
        """
        tbCli=TablaServicios()
        tbCli.show_all()

class TablaServicios(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Listado Servicios")
        self.set_default_size(400,300)

        self.set_border_width(10)

        self.grid=Gtk.Grid()
        self.grid.set_column_spacing(10)
        self.grid.set_row_spacing(10)

        self.cajaVentana = Gtk.Box(spacing=20)
        self.cajaVentana.set_orientation(Gtk.Orientation.VERTICAL)

        self.add(self.cajaVentana)
        self.cajaVentana.add(self.grid)

        self.lblMatri=Gtk.Label("Matricula: ")
        self.lsMatri=Gtk.ComboBoxText()
        self.lsMatri.set_entry_text_column(0)
        self.btnConsultar=Gtk.Button("Consultar")
        self.btnConsultar.connect("clicked", self.on_consulta_clicked)
        self.btnMostrar=Gtk.Button("Mostrar Todos")
        self.btnMostrar.connect("clicked", self.on_mostrar_click)
        self.btnInforme=Gtk.Button("Crear Factura")
        self.btnInforme.connect("clicked", self.on_factura)

        self.grid.attach(self.lblMatri,0,0,1,1)
        self.grid.attach(self.lsMatri,1,0,1,1)
        self.grid.attach(self.btnConsultar,2,0,1,1)
        self.grid.attach(self.btnMostrar,3,0,1,1)
        self.grid.attach(self.btnInforme,4,0,1,1)
        self.matricula_pieza()

        ##Tabla Clientes
        self.columnas = ["ID", "Matricula", "Nombre", "Precio", "Marca", "Procedencia", "Año Fabricacion"]
        self.modelo = Gtk.ListStore(str, str, str, int, str, str, str)
        self.axenda = []
        self.vista = Gtk.TreeView(model=self.modelo)

        for i in range(len(self.columnas)):
            celda = Gtk.CellRendererText()
            self.columna = Gtk.TreeViewColumn(self.columnas[i], celda, text=i)
            self.vista.append_column(self.columna)

        self.cajaVentana.add(self.vista)

    def on_factura(self,btnIn):
        tiendaRe=sqlite3.connect("BaseTiendaRecambios.dat")
        cursor=tiendaRe
        resultCli= cursor.execute("select * from Clientes where Matricula='"+self.lsMatri.get_active_text()+"'")
        lista=[]
        for elemento in resultCli:
            lista.append(elemento)

        resultPro=cursor.execute("select * from Productos where Matriculas='"+self.lsMatri.get_active_text()+"'")

        listaP=[]
        for elementos in resultPro:
            listaP.append(elementos)
        cursor.close()
        InformeFactura.informeFactura(lista,listaP)

    def matricula_pieza(self):
        """
        Lista las matriculas para poder consultar despues por el combobox
        :return: nothing
        """
        tiendaC=sqlite3.connect("BaseTiendaRecambios.dat")
        cursor=tiendaC.cursor()
        try:

            cursor.execute("select Matricula from Clientes")
            for rexistro in cursor.fetchall():
                self.lsMatri.append_text(rexistro[0])
        finally:
            cursor.close()
            tiendaC.close()
    def on_consulta_clicked(self,btnConsu):
        """
        Consultar gracias al combobox visualiza productos segun la matricula selecionada.
        :param btnConsu:
        :return: nothing
        """

        tiendaC = sqlite3.connect("BaseTiendaRecambios.dat")
        cursor = tiendaC.cursor()
        try:
            cursor.execute("select * from Productos WHERE Matriculas='"+self.lsMatri.get_active_text()+"'")
            self.axenda.clear()

            for rexistro in cursor.fetchall():
                self.axenda.append(
                    [rexistro[0], rexistro[1], rexistro[2], rexistro[3], rexistro[4], rexistro[5], rexistro[6]])
            self.modelo.clear()
            for elemento in self.axenda:
                self.modelo.append(elemento)


        finally:
            cursor.close()
            tiendaC.close()

    def on_mostrar_click(self,btMostrar):
        """
        Muestra todos los productos de la base de datos
        :param btMostrar:
        :return: nothing
        """
        self.columnas.clear()
        tiendaC = sqlite3.connect("BaseTiendaRecambios.dat")
        cursor = tiendaC.cursor()
        try:
            cursor.execute("select * from Productos")
            self.axenda.clear()
            for rexistro in cursor.fetchall():
                self.axenda.append(
                    [rexistro[0], rexistro[1], rexistro[2], rexistro[3], rexistro[4], rexistro[5], rexistro[6]])
            self.modelo.clear()
            for elemento in self.axenda:
                self.modelo.append(elemento)




        finally:
            cursor.close()
            tiendaC.close()



if __name__ == '__main__':
    form=FormularioInicio()
    Gtk.main()
