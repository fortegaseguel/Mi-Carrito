from kivy.lang import Builder
from kivymd.app import MDApp
import sqlite3

kv = """
MDFloatLayout:
    BoxLayout:
        orientation: "vertical"
        size: root.width, root.height
        
        Label:
            id: word_label
            text_size: self.size
            halign: "center"
            text: "Enter a name"
            font_size: 32

        TextInput:
            id: word_input
            multiline: False
            size_hint: (1,.5)

        Button:
            size_hint: (1, 0.5)
            font_size: 32
            text: "Submit Name"
            on_press: app.submit()

        Button:
            size_hint: (1, 0.5)
            font_size: 32
            text: "Show Records"
            on_press: app.show_records()

        Button:
            size_hint: (1, 0.5)
            font_size: 32
            text: "Delete Records"
            on_press: app.delete_records()
"""



class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_pallete = "BlueGray"

        # Create Database or connect it
        conn = sqlite3.connect('mydatabase.db')

        # Create a Cursor
        c = conn.cursor()

        #Create Table
        sql = f"""
            CREATE TABLE if not exists customers(
                name text
            )
        """
        c.execute(sql)

        # Commit Changes
        conn.commit()

        #Close Conection
        conn.close()

        return Builder.load_string(kv)



    def submit(self):
        # Create Database or connect it
        conn = sqlite3.connect('mydatabase.db')

        # Create a Cursor
        c = conn.cursor()


        #Add a Record
        c.execute("INSERT INTO customers VALUES (:first)",
            {
                'first': self.root.ids.word_input.text,
            })


        # Add a message
        self.root.ids.word_label.text = f'{self.root.ids.word_input.text} added'

        # Clear Inputs
        self.root.ids.word_input.text = ''


        # Commit Changes
        conn.commit()


        #Close Conection
        conn.close()



    def show_records(self):
        # Create Database or connect it
        conn = sqlite3.connect('mydatabase.db')

        # Create a Cursor
        c = conn.cursor()


        # Grab records from database
        sql = """
            SELECT * FROM customers
        """
        c.execute(sql)
        records = c.fetchall()

        word = ''


        # Loop thru records
        for record in records:
            word = f'{word}\n{record[0]}'
            self.root.ids.word_label.text = f'{word}'


        # Commit Changes
        conn.commit()


        #Close Conection
        conn.close()


    def delete_records(self):
        # Create Database or connect it
        conn = sqlite3.connect('mydatabase.db')

        # Create a Cursor
        c = conn.cursor()


        #Add a Record
        c.execute("DELETE FROM customers")


        # Add a message
        self.root.ids.word_label.text = 'All records are deleted'

        # Clear Inputs
        self.root.ids.word_input.text = ''


        # Commit Changes
        conn.commit()


        #Close Conection
        conn.close()

MainApp().run()
