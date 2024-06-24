import requests
from bs4 import BeautifulSoup

url = "https://www.cambioschaco.com.py"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="table table-hover cotiz-tabla")
    
    if table:
        data = []
        rows = table.find_all("tr")[1:]
        
        for row in rows:
            cols = row.find_all("td")
            
            moneda = cols[0].text.strip()
            
            if moneda == "US Dollar":
                monedas = "USD"
            elif moneda == "Brazilian Real":
                monedas = "BRL"
            elif moneda == "Argentine Peso":
                monedas = "ARS"
            elif moneda == "Euro":
                monedas = "EUR"
            elif moneda == "Chilean Peso":
                monedas = "CLP"
            elif moneda == "Uruguayan Peso":
                monedas = "UYU"
            elif moneda == "Colombian Peso":
                monedas = "COP"
            elif moneda == "Mexican Peso":
                monedas = "MXN"
            elif moneda == "Bolivian Boliviano":
                monedas = "BOB"
            elif moneda == "Peruvian Nuevo Sol":
                monedas = "PEN"
            elif moneda == "Canadian Dollar":
                monedas = "CAD"
            elif moneda == "Australian Dollar":
                monedas = "AUD"
            elif moneda == "Norwegian Krone":
                monedas = "NOK"
            elif moneda == "Danish Krone":
                monedas = "DKK"
            elif moneda == "Swedish Krona":
                monedas = "SEK"
            elif moneda == "British Pound Sterling":
                monedas = "GBP"
            elif moneda == "Swiss Franc":
                monedas = "CHF"
            elif moneda == "Japanese Yen":
                monedas = "JPY"
            elif moneda == "Kuwaiti Dinar":
                monedas = "KWD"
            elif moneda == "Israeli New Sheqel":
                monedas = "ILS"
            elif moneda == "South African Rand":
                monedas = "ZAR"
            elif moneda == "Russian Ruble":
                monedas = "RUB"
            
            compra = float(cols[1].text.strip().replace(",", ""))
            venta = float(cols[2].text.strip().replace(",", ""))

            spread = venta - compra

            item = {
                "moneda": moneda,
                "codigo": monedas,
                "compra": compra,
                "venta": venta,
                "spread": spread
            }
            
            data.append(item)
        
        for x in data:
            print(f"""
                {x}
            """)
    
    else:
        print("No se encontró la tabla de cotizaciones en la página.")

else:
    print(f"Error al realizar la solicitud. Código de estado: {response.status_code}")
