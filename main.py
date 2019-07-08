from tkinter import *
from tkinter import ttk

import configparser
import json
import requests

DEFAULTPADDING = 4

class Exchanger(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, width= "400", height="150")
        config = configparser.ConfigParser()
        config.read("config.ini")

        #accede a config para acceder a la API
        self.api_key = config['fixer.io']['API_KEY']
        self.all_symbols_ep = config['fixer.io']['ALL_SYMBOLS_EP']
        self.rate_ep = config['fixer.io']['RATE_LATEST_EP']

        currencies = self.getCurrencies() #pedir las monedas a la API

        #Variables de control
        self.strInQuantity = StringVar(value="") #aqui guardamos la info de la cantidad
        self.strInQuantity.trace('w', self.convertirDivisas) #sigue el stringvar cada vez que se modifica (w es cada vez que hay cambios)
        self.strInCurrency = StringVar() #aquí guardamos la selección de los deplegables
        self.strOutCurrency = StringVar()


        self.pack_propagate(0) #para que mantenga el ancho y alto del __init__
        frInCurrency = ttk.Frame(self) # instancia de ttkFrame, para los Input
        frInCurrency.pack_propagate(0) 
        

        lblQ = ttk.Label(frInCurrency, text="cantidad") #hereda de  incurrency para que se coloque ahí
        lblQ.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady= DEFAULTPADDING)

        self.inQuantityEntry = ttk.Entry(frInCurrency, font=('Helvetica', 24, 'bold'), width=10, textvariable=self.strInQuantity) 
        self.inQuantityEntry.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady= DEFAULTPADDING) #te lo pone debajo del anterior

        self.inCurrencyCombo = ttk.Combobox(frInCurrency, width=25, height=5, values=currencies, textvariable=self.strInCurrency) #desplegable
        self.inCurrencyCombo.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady= DEFAULTPADDING)
        self.inCurrencyCombo.bind('<<ComboboxSelected>>', self.convertirDivisas)

        frInCurrency.pack(side=LEFT, fill=BOTH, expand=True) # se expande en la izquierda, y el expand es en vertical


        frOutCurrency = ttk.Frame(self) # instancia de ttkFrame, para los Input
        frOutCurrency.pack_propagate(0) 

        lblQ = ttk.Label(frOutCurrency, text="cantidad") 
        lblQ.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady= DEFAULTPADDING)

        self.outQuantityLbl = ttk.Label(frOutCurrency, font=('Helvetica', 26), anchor=E, width=10)
        self.outQuantityLbl.pack (side=TOP, fill=X, padx=DEFAULTPADDING, pady= DEFAULTPADDING, ipady=2)

        self.outCurrencyCombo = ttk.Combobox(frOutCurrency, width=25, height=5, values=currencies, textvariable=self.strOutCurrency)
        self.outCurrencyCombo.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING)
        self.outCurrencyCombo.bind('<<ComboboxSelected>>', self.convertirDivisas)

        frOutCurrency.pack(side=LEFT, fill=BOTH, expand=True) # como arriba ya hay una en la izquierda se pondra a la derecha

    def convertirDivisas(self, *args):
        print("in: ", self.strInCurrency.get())
        print("out: ", self.strOutCurrency.get())
        print("Cantidad: ", self.strInQuantity.get())


    def getCurrencies(self):
        response = requests.get(self.all_symbols_ep.format(self.api_key))

        if response.status_code == 200:
            currencies = json.loads(response.text) # json hace que nos devuelva un diccionario que entiende python
            result = []
            symbols = currencies['symbols']

            for symbol in symbols:
                text = "{} - {}".format(symbol, symbols[symbol])
                result.append(text)

            return result
        else:
            print("se ha producido un error al consultar symbols:", response.status_code )


            


class MainApp (Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("400x150")
        self.title("Exchanger fixer.io")
        self.exchanger = Exchanger(self)
        self.exchanger.place(x=0, y=0)

    def start(self):
        self.mainloop()


if __name__ == '__main__':
    exchanger = MainApp()
    exchanger.start()





