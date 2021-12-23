from android.permissions import request_permissions, Permission
from kivy.config import Config
from baseclasses.reportes import *
from baseclasses.ventas import *
from baseclasses.compras import *
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"


Config.set("graphics", "width", "340")
Config.set("graphics", "hight", "640")


Builder.load_file('kvs/main.kv')
Builder.load_file('kvs/compras.kv')
Builder.load_file('kvs/ventas.kv')
Builder.load_file('kvs/reportes.kv')


class MainWid(ScreenManager):
    def __init__(self, **kwargs):
        super(MainWid, self).__init__()
        self.APP_PATH = os.getcwd()
        self.DB_PATH = self.APP_PATH+'/database/carrito.db'

######### M O D U L O   D E   I N I C I O #########

        self.StartWid = StartWid(self)
        wid = Screen(name='start')
        wid.add_widget(self.StartWid)
        self.add_widget(wid)

######### M O D U L O   D E   R E P O R T E S #########

        self.ReportesWid = ReportesWid(self)
        self.Popup = SuccessPopup()

        wid = Screen(name='reportes')
        wid.add_widget(self.ReportesWid)
        self.add_widget(wid)


######### M O D U L O   D E   C O M P R A S #########

        self.DataBaseWidCompras = DataBaseWidCompras(self)
        self.InsertDataWidCompras = BoxLayout()
        self.UpdateDataWidCompras = BoxLayout()
        self.Popup = MessagePopup()

        wid = Screen(name='database_compras')
        wid.add_widget(self.DataBaseWidCompras)
        self.add_widget(wid)

        wid = Screen(name='insertdata_compras')
        wid.add_widget(self.InsertDataWidCompras)
        self.add_widget(wid)

        wid = Screen(name='updatedata_compras')
        wid.add_widget(self.UpdateDataWidCompras)
        self.add_widget(wid)


######### M O D U L O   D E   V E N T A S #########

        self.DataBaseWidVentas = DataBaseWidVentas(self)
        self.InsertDataWidVentas = BoxLayout()

        wid = Screen(name='database_ventas')
        wid.add_widget(self.DataBaseWidVentas)
        self.add_widget(wid)

        wid = Screen(name='insertdata_ventas')
        wid.add_widget(self.InsertDataWidVentas)
        self.add_widget(wid)

        self.goto_start()


######### I N I C I O #########


    def goto_start(self):
        self.current = 'start'
        InsertDataWidVentas.list.clear()


######### R E P O R T E S #########


    def goto_reportes(self):
        self.current = 'reportes'


######### M O D U L O   D E   C O M P R A S #########


    def goto_database_compras(self):
        self.DataBaseWidCompras.check_memory_insumos()
        self.current = 'database_compras'

    def goto_insertdata_compras(self):
        self.InsertDataWidCompras.clear_widgets()
        wid = InsertDataWidCompras(self)
        self.InsertDataWidCompras.add_widget(wid)
        self.current = 'insertdata_compras'

    def goto_updatedata_compras(self, data_id):
        self.UpdateDataWidCompras.clear_widgets()
        wid = UpdateDataWidCompras(self, data_id)
        self.UpdateDataWidCompras.add_widget(wid)
        self.current = 'updatedata_compras'


######### M O D U L O   D E   V E N T A S #########


    def goto_database_ventas(self):
        self.DataBaseWidVentas.check_memory_ventas()
        self.current = 'database_ventas'

    def goto_insertdata_ventas(self):
        self.InsertDataWidVentas.clear_widgets()
        wid = InsertDataWidVentas(self)
        self.InsertDataWidVentas.add_widget(wid)
        self.current = 'insertdata_ventas'


# PANTALLA DE INICIO

class StartWid(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(StartWid, self).__init__()
        self.mainwid = mainwid

    def create_database_compras(self):
        connect_to_database(self.mainwid.DB_PATH)
        self.mainwid.goto_database_compras()

    def create_database_ventas(self):
        connect_to_database(self.mainwid.DB_PATH)
        self.mainwid.goto_database_ventas()


# MAIN APP

class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Mi Carrito"
        super().__init__(**kwargs)

    def open_settings(self, *largs):
        pass

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.theme_style = "Dark"

        return MainWid()

    def on_start(self):
        request_permissions(
            [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])


if __name__ == '__main__':
    MainApp().run()
