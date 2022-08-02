import json
import requests
import pandas as pd
from datetime import datetime


def get_portfolio(data, fund):
    fecha_fondo = data['data'][0]['dataXML']['Cabecera']['FechaReporte']
    nombre_fondo = data['data'][0]['dataXML']['Cabecera']['FondoNombre']
    company = data['data'][0]['dataXML']['Cabecera']['SGNombre']
    # Create a dictionary for each fund each day
    cartera = {}
    cartera['Api'] = fund
    cartera['Fecha'] = fecha_fondo
    cartera['Nombre_Fondo'] = nombre_fondo

    return fund, fecha_fondo, nombre_fondo


def fetchPortfolio(fund):
    api = "https://api.cafci.org.ar/interfaz/semanal/resumen/cartera/"
    website = api+str(fund)
    r = requests.get(website)
    status_code = r.status_code
    data = r.json()
    status_code = r.status_code
    fund, fecha_fondo, nombre_fondo = get_portfolio(data, fund)
    return fund, fecha_fondo, nombre_fondo, status_code, data


with open('start_fund.json', 'r') as infile:
    fund = json.load(infile)
    print('fund', fund)
infile.close()

fund, fecha_fondo, nombre_fondo , status_code , data = fetchPortfolio(fund)

while (status_code == 200 and data["success"]):

    print(fund, fecha_fondo)

    try:
        url = 'https://portdatapy.herokuapp.com/funds/add'
        myobj = {'Api': fund , 'Nombre_Fondo': nombre_fondo , "Fecha": fecha_fondo}
        requests.post(url, json = myobj)

        fund = fund + 1

        fund, fecha_fondo, nombre_fondo , status_code, data = fetchPortfolio(fund)

        with open('start_fund.json', 'w') as start_fund:
            json.dump(fund, start_fund)
        start_fund.close()

    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        break

