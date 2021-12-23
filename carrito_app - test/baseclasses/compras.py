from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.popup import Popup
import sqlite3

def connect_to_database(path):
    try:
        con = sqlite3.connect(path)
        cursor = con.cursor()
        create_table_insumos(cursor)
        con.commit()
        con.close()
    except Exception as e:
        print(e)


def create_table_insumos(cursor):
    cursor.execute(
        '''
        CREATE TABLE if not exists insumos(
        id INTEGER, 
        producto VARCHAR(100),
        cantidad INTEGER,
        unidad VARCHAR(5),
        categoria VARCHAR(100),
        costo INTEGER,
        fecha DATE DEFAULT(DATE('now', 'localtime')),
        PRIMARY KEY(id AUTOINCREMENT)
        )'''
    )


class MessagePopup(Popup):
    pass




class DataBaseWidCompras(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(DataBaseWidCompras, self).__init__()
        self.mainwid = mainwid

    def check_memory_insumos(self):
        self.ids.container.clear_widgets()
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        cursor.execute(
            'select ID, producto, cantidad, unidad, categoria, costo, fecha from insumos')

        lista = cursor.fetchall()
        lista.reverse()

        for i in lista:
            wid = DataWidCompras(self.mainwid)
            r0 = '\n'
            r1 = f'id: {i[0]}\n'
            r2 = f'Producto: {i[1]}\n'
            r3 = f'En almacen: {i[2]} {i[3]}\n'
            r4 = f'Categoria: {i[4]}\n'
            r5 = f'Costo por unidad: ${i[5]}\n'
            r6 = f'Fecha de Ingreso: {i[6]}\n'
            wid.data_id = str(i[0])
            wid.data = r0+r1+r2+r3+r4+r5+r6
            self.ids.container.add_widget(wid)

        con.close()

    def create_new_product(self):
        self.mainwid.goto_insertdata_compras()

class UpdateDataWidCompras(BoxLayout):
    def __init__(self, mainwid, data_id, **kwargs):
        super(UpdateDataWidCompras, self).__init__()
        self.mainwid = mainwid
        self.data_id = data_id
        self.check_memory_insumos()

    def check_memory_insumos(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        s = 'select ID, producto, cantidad, unidad, categoria, costo from insumos where ID='
        cursor.execute(s+self.data_id)

        for i in cursor:
            self.ids.ti_producto.text = i[1]
            self.ids.ti_cantidad.text = str(i[2])
            self.ids.ti_unidad.text = i[3]
            self.ids.ti_categoria.text = i[4]
            self.ids.ti_costo.text = str(i[5])
        con.close()


    def select_unidad(self, value):
        self.ids.ti_unidad.text = f'{value}'

    def select_categoria(self, value):
        self.ids.ti_categoria.text = f'{value}'


    def update_data_compras(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()

        d1 = str(self.ids.ti_producto.text)
        d2 = str(self.ids.ti_cantidad.text)
        d3 = str(self.ids.ti_unidad.text)
        d4 = str(self.ids.ti_categoria.text)
        d5 = str(self.ids.ti_costo.text)

        a1 = (d1, d2, d3, d4, d5)
        s1 = 'UPDATE insumos SET'
        s2 = 'producto= "%s",cantidad= "%s", unidad= "%s", categoria= "%s", costo= "%s"' % a1
        s3 = 'WHERE ID= %s' % self.data_id

        try:
            cursor.execute(s1+' '+s2+' '+s3)
            con.commit()
            con.close()
            self.mainwid.goto_database_compras()
        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Data base error"

            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else:
                message.text = str(e)
            con.close()

    def delete_data(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        s = 'delete from insumos where ID='+self.data_id
        cursor.execute(s)
        con.commit()
        con.close()
        self.mainwid.goto_database_compras()

    def back_to_dbw(self):
        self.mainwid.goto_database_compras()


class InsertDataWidCompras(TabbedPanel):
    def __init__(self, mainwid, **kwargs):
        super(InsertDataWidCompras, self).__init__()
        self.mainwid = mainwid

    def ingreso_rapido(self, value):
        self.ids.ti_categoria.text = f'{value}'


    def insert_datafast(self):
        if self.ids.ti_categoria.text == 'Pack Bebidas':
            d1 = self.ids.ti_producto_rapido.text
            d2 = self.ids.ti_cantidadd.text
            d3 = 'Un'
            d4 = 'Bebidas'
            d5 = self.ids.ti_costoo.text

            a1 = (d1,d2,d3,d4,d5)
            print(a1)

        elif self.ids.ti_categoria.text == 'Papas Fritas':
            d1 = self.ids.ti_producto_rapido.text
            d2 = self.ids.ti_cantidadd.text
            d3 = 'Kg'
            d4 = 'Congelados'
            d5 = self.ids.ti_costoo.text

            a1 = (d1,d2,d3,d4,d5)
            print(a1)

        elif self.ids.ti_categoria.text == 'Proteina Congelada':
            d1 = self.ids.ti_producto_rapido.text
            d2 = self.ids.ti_cantidadd.text
            d3 = 'Kg'
            d4 = 'Congelados'
            d5 = self.ids.ti_costoo.text

            a1 = (d1,d2,d3,d4,d5)
            print(a1)

        elif self.ids.ti_categoria.text == 'Pan':
            d1 = self.ids.ti_producto_rapido.text
            d2 = self.ids.ti_cantidadd.text
            d3 = 'Un'
            d4 = 'Pan'
            d5 = self.ids.ti_costoo.text

            a1 = (d1,d2,d3,d4,d5)
            print(a1)

        elif self.ids.ti_categoria.text == 'Fajitas':
            d1 = self.ids.ti_producto_rapido.text
            d2 = self.ids.ti_cantidadd.text
            d3 = 'Un'
            d4 = 'Pan'
            d5 = self.ids.ti_costoo.text

            a1 = (d1,d2,d3,d4,d5)
            print(a1)

        elif self.ids.ti_categoria.text == 'Verduras':
            d1 = self.ids.ti_producto_rapido.text
            d2 = self.ids.ti_cantidadd.text
            d3 = 'Kg'
            d4 = 'No Congelados'
            d5 = self.ids.ti_costoo.text

            a1 = (d1,d2,d3,d4,d5)
            print(a1)

        elif self.ids.ti_categoria.text == 'Bencina':
            d1 = self.ids.ti_producto_rapido.text
            d2 = self.ids.ti_cantidadd.text
            d3 = 'Lts'
            d4 = 'Combustible'
            d5 = self.ids.ti_costoo.text

            a1 = (d1,d2,d3,d4,d5)
            print(a1)

        elif self.ids.ti_categoria.text == 'Pago Jornada':
            d1 = self.ids.ti_producto_rapido.text
            d2 = self.ids.ti_cantidadd.text
            d3 = 'Un'
            d4 = 'Personal'
            d5 = self.ids.ti_costoo.text

            a1 = (d1,d2,d3,d4,d5)
            print(a1)


        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()

        s1 = 'INSERT INTO insumos(producto, cantidad, unidad, categoria, costo)'
        s2 = 'VALUES("%s", "%s", "%s", "%s", "%s")' % a1

        try:
            cursor.execute(s1+' '+s2)
            con.commit()
            con.close()
            self.mainwid.goto_insertdata_compras()

        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Data base error"

            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else:
                message.text = str(e)
            con.close()



    def select_unidad(self, value):
        self.ids.ti_unidad.text = f'{value}'
    
    def select_categoria(self, value):
        self.ids.ti_categoria.text = f'{value}'

    def insert_data(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()

        d1 = self.ids.ti_producto.text
        d2 = self.ids.ti_cantidad.text
        d3 = self.ids.ti_unidad.text
        d4 = self.ids.ti_categoria.text
        d5 = self.ids.ti_costo.text

        a1 = (d1, d2, d3, d4, d5)
        s1 = 'INSERT INTO insumos(producto, cantidad, unidad, categoria, costo)'
        s2 = 'VALUES("%s", "%s", "%s", "%s", "%s")' % a1

        try:
            cursor.execute(s1+' '+s2)
            con.commit()
            con.close()
            self.mainwid.goto_insertdata_compras()

        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Data base error"

            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else:
                message.text = str(e)
            con.close()

    def back_to_dbw(self):
        self.mainwid.goto_database_compras()


class DataWidCompras(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(DataWidCompras, self).__init__()
        self.mainwid = mainwid

    def update_data_compras(self, data_id):
        self.mainwid.goto_updatedata_compras(data_id)

