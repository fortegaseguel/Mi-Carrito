from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
import sqlite3


def connect_to_database(path):
    try:
        con = sqlite3.connect(path)
        cursor = con.cursor()
        create_table_ventas(cursor)
        con.commit()
        con.close()
    except Exception as e:
        print(e)


def create_table_ventas(cursor):
    cursor.execute(
        '''
        CREATE TABLE if not exists ventas(
        id INTEGER, 
        pedido VARCHAR(100),
        total INTEGER,
        formadepago VARCHAR(5),
        fecha DATE DEFAULT(DATE('now', 'localtime')),
        PRIMARY KEY(id AUTOINCREMENT)
        )'''
    )


class DataBaseWidVentas(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(DataBaseWidVentas, self).__init__()
        self.mainwid = mainwid

    def check_memory_ventas(self):
        self.ids.container_x.clear_widgets()
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        cursor.execute(
            'select ID, pedido, total, formadepago, fecha from ventas')

        lista = cursor.fetchall()
        lista.reverse()

        for i in lista:
            wid = DataWidVentas(self.mainwid)
            r0 = '\n\n'

            r1 = f'id: {i[0]}\n'
            r2 = f'Pedido: {i[1]}\n'
            r3 = f'Total: ${i[2]}\n'
            r4 = f'Forma de Pago: {i[3]}\n'
            r5 = f'Fecha de Ingreso: {i[4]}\n\n'
            wid.data_id = str(i[0])
            wid.data = r0+r1+r2+r3+r4+r5
            self.ids.container_x.add_widget(wid)

        con.close()

    def create_new_product(self):
        self.mainwid.goto_insertdata_ventas()


class InsertDataWidVentas(TabbedPanel):
    def __init__(self, mainwid, **kwargs):
        super(InsertDataWidVentas, self).__init__()
        self.mainwid = mainwid

    list = []
    sumalist = []
    total = 0
    metodopago = ''

    def checkbox_click(self, instance, value, seleccion, qty, layout, precio):
        print()
        try:
            sub = str(int(qty)*precio)
            a = (seleccion + ' : ' + qty + ' == ' + "$" + sub)

            if value == True:
                layout.opacity = 1

                for item in InsertDataWidVentas.list:
                    if seleccion in item:
                        InsertDataWidVentas.list.remove(item)

                InsertDataWidVentas.list.append(a)
                InsertDataWidVentas.sumalist.append(precio)

                comanda = "\n".join(InsertDataWidVentas.list)
                self.ids.output_label.text = f'{comanda}'

                total = sum(InsertDataWidVentas.sumalist)
                self.ids.a_pagar.text = str(total)
                if total <= 0:
                    total = 0
                    self.ids.a_pagar.text = str(total)

                print(InsertDataWidVentas.list, total)

            else:
                InsertDataWidVentas.list.remove(a)
                InsertDataWidVentas.sumalist.remove(precio)

                comanda = "\n".join(InsertDataWidVentas.list)
                self.ids.output_label.text = f'{comanda}'

                total = sum(InsertDataWidVentas.sumalist)
                self.ids.a_pagar.text = str(total)
                if total <= 0:
                    total = 0
                    self.ids.a_pagar.text = str(total)

                print(InsertDataWidVentas.list, total)

                layout.opacity = 0

        except Exception as e:
            print(e)

    def mediodepago(self, instance, value, metodo):
        if value == True:
            InsertDataWidVentas.metodopago = metodo
            print(InsertDataWidVentas.metodopago)
        else:
            InsertDataWidVentas.metodopago = ''
            print(InsertDataWidVentas.metodopago)


# Guarda el pedido en la base de datos

    def insert_data(self):
        con = sqlite3.connect('database/carrito.db')
        cursor = con.cursor()
        lista = InsertDataWidVentas.list

        print(f'list = {lista}')

        d1 = "\n".join(lista)
        d2 = self.ids.a_pagar.text
        d3 = InsertDataWidVentas.metodopago

        a1 = (d1, d2, d3)
        print(f'a1 = {a1}')
        s1 = 'INSERT INTO ventas(pedido, total, formadepago)'
        s2 = 'VALUES("%s", "%s", "%s")' % a1

        cursor.execute(s1+' '+s2)
        con.commit()
        con.close()

        InsertDataWidVentas.list.clear()
        InsertDataWidVentas.sumalist.clear()
        self.mainwid.goto_database_ventas()

    def back_to_dbw(self):
        InsertDataWidVentas.list.clear()
        InsertDataWidVentas.sumalist.clear()
        self.mainwid.goto_database_ventas()


class DataWidVentas(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(DataWidVentas, self).__init__()
        self.mainwid = mainwid

    def update_data_ventas(self, data_id):
        self.mainwid.goto_updatedata_ventas(data_id)

    def delete_data(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        s = 'delete from ventas where ID='+self.data_id
        cursor.execute(s)
        con.commit()
        con.close()

        self.mainwid.goto_database_ventas()
