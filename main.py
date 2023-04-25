# INFO: https://smn.conagua.gob.mx/es/web-service-api
import requests
import gzip
import shutil
import json
import smtplib
import os
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get("GOOGLE_USER")    #LEEMOS EN CORREO GUARDADO EN LAS VARIABLES DEL SISTEMA (LINUX EN MI CASO PARTICULAR)
EMAIL_PASSWORD = os.environ.get("GOOGLE_PASS")   #LEEMOS LA CONTRASEÑA EN LAS VARIABLES DEL SISTEMA (LINUX EN MI CASO PARTICULAR)

def email(to, subject, content):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to
    msg.set_content(content)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
def ListaEstados(json):
    holder = {}
    for estado in json:
        for i in range(1,33):
            if estado["ides"] == str(i):
                if str(i) not in holder:
                    holder[str(i)] = estado["nes"]
    sorted_list = sorted(holder.items(), key=lambda x: x[1])
    def print_estados():
        for i in sorted_list:
            print("Nombre Estado: {}, ID: {}".format(i[1], i[0]))
    return print_estados()

def ListaMunicipiosEstado(id_estado, json):
    holder = {}
    for estado in json:
        if estado["ides"] == str(id_estado):
            if estado["idmun"] not in holder:
                holder[estado["idmun"]] = estado["nmun"]
    sorted_list = sorted(holder.items(), key=lambda x: x[1])
    def print_municipios():
        for i in sorted_list:
            print("Nombre Municipio: {}, ID: {}".format(i[1], i[0].ljust(15)))
    return print_municipios()

class municipioData:

    def __init__(self, municipio :dict):
        self.cc = municipio["cc"]
        self.desciel = municipio["desciel"]
        self.dirvienc = municipio["dirvienc"]
        self.dirvieng = municipio["dirvieng"]
        self.dloc = municipio["dloc"]
        self.ides = municipio["ides"]
        self.idmun = municipio["idmun"]
        self.lat = municipio["lat"]
        self.lon = municipio["lon"]
        self.ndia = municipio["ndia"]
        self.nes = municipio["nes"]
        self.nmun = municipio["nmun"]
        self.prec = municipio["prec"]
        self.probprec = municipio["probprec"]
        self.raf = municipio["raf"]
        self.tmax = municipio["tmax"]
        self.tmin = municipio["tmin"]
        self.velvien = municipio["velvien"]

    def __str__(self):
        text = f""" 
            Nombre de Estado: {self.nes}
            Nombre de Municipio: {self.nmun}
            Número de día: {self.ndia}
            Id estado: {self.ides}
            Id municipio: {self.idmun}
            Temperatura máxima (°C): {self.tmax}
            Temperatura mímima (°C): {self.tmin}
            Probabilidad de precipitación (%): {self.probprec}
            Precipitación (litros/m2): {self.prec}
            Cobertura de nubes (%): {self.cc}
            Descripción del cielo: {self.desciel}
            Dirección del viento (Cardinal): {self.dirvienc}
            Dirección del viento (Grados): {self.dirvieng}
            Velocidad del viento (km/h): {self.velvien}
            Día local, inicia cuatro horas antes: {self.dloc}
            Latitud: {self.lat}
            Longitud: {self.lon}
            Diferencia respecto a hora UTC ?: {self.raf}
        """
        return text

    def print_terminal(self):
        print("{}, {}".format(self.nes, self.nmun))
        print("Número de día: {}".format(self.ndia))
        print("Id estado: {}".format(self.ides))
        print("Id municipio: {}".format(self.idmun))
        print("Temperatura máxima (°C): {}".format(self.tmax))
        print("Temperatura mímima (°C): {}".format(self.tmin))
        print("Probabilidad de precipitación (%): {}".format(self.probprec))
        print("Precipitación (litros/m2): {}".format(self.prec))
        print("Cobertura de nubes (%): {}".format(self.cc))
        print("Descripción del cielo: {}".format(self.desciel))
        print("Dirección del viento (Cardinal): {}".format(self.dirvienc))
        print("Dirección del viento (Grados): {}".format(self.dirvieng))
        print("Velocidad del viento (km/h): {}".format(self.velvien))
        print("Día local, inicia cuatro horas antes: {}".format(self.dloc))
        print("Latitud: {}".format(self.lat))
        print("Longitud: {}".format(self.lon))
        print("Diferencia respecto a hora UTC ?: {}".format(self.raf))

def datosMeteorologicos(id_estado, id_municipio, dia, json):
    for estado in json:
        if estado["ides"] == id_estado:
            if estado["idmun"] == id_municipio:
                if estado["ndia"] == dia:
                    mun_info = municipioData(estado)
                    mun_info.print_terminal()
                    print("")
    return mun_info

if __name__ == '__main__':

    # Headers se agregaron ya que si se manda el request sin ellos en servidor regresa un status de 403
    url = "https://smn.conagua.gob.mx/webservices/?method=1"
    headers = {
        'Host': 'smn.conagua.gob.mx',
        #'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    }

    filename = "DailyForecast_MX.gz"
    json_file = "DailyForecast_MX.json"
    with open(filename, "wb") as f:
        r = requests.get(url, headers=headers)
        f.write(r.content)
    with gzip.open(filename, 'rb') as f_in:
        with open(json_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    with open(json_file) as json_file:
        r_json = json.load(json_file)

    s = str
    n = str
    e = str
    m = str
    d = str
    print("Si desea conocer los datos del clima de algun municipio de la republica, debe saber la ID del municipio y la ID del estado en el que se encuentra dicho municipio.")
    print("Requiere se mueste una lista de Estados de la Republica con su ID? (Si, No):")

    s = input()
    if s == "Si":
        ListaEstados(r_json)

    print("Requiere se mueste una lista de municipios con su ID pertenecientes a un estado en especifico? (Si, No):")
    s = input()
    if s == "Si":
        print("Por favor escriba la ID del estado del cual quiere obtener la lista de municipios:")
        n = input()
        ListaMunicipiosEstado(n, r_json)

    print("Se pude dar la informacion del clima para el dia de hoy y a 3 dias, Por favor ingrese numero '0' para el dia de hoy, el numero '1' para el dia de mañana y asi sucesivamente(rango de 0 al 3)")
    d = input()

    print("Ahora que ya sabe la ID del municipio y del estado, por favor ingrese primero la ID del estado seguido de la ID del municipio para obtener los datos del clima:")
    print("ID estado:")
    e = input()
    print("ID municipio:")
    m = input()
    print("Usted escribio estado con ID: {}, y municipio con ID: {}".format(e, m))
    email(<AQUI TU CORREO>, "Clima", f"{  datosMeteorologicos(e,m, d,r_json)  } ")


