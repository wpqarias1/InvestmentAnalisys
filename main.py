from yahooquery import Ticker
import json
import time

# Aquí pones las acciones que quieres vigilar
mis_acciones = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']

def ejecutar_app():
    print("Iniciando consulta a Yahoo Finance...")
    # 'Ticker' es la herramienta que habla con Yahoo
    t = Ticker(mis_acciones)
    
    # Obtenemos los datos fundamentales
    ratios = t.summary_detail
    
    datos_finales = []
    
    for ticker in mis_acciones:
        # Extraemos el P/E Ratio y el precio
        info = ratios.get(ticker, {})
        pe = info.get('trailingPE', 'N/A')
        precio = info.get('previousClose', 'N/A')
        
        datos_finales.append({
            "ticker": ticker,
            "pe_ratio": pe,
            "precio": precio
        })
        print(f"Datos de {ticker} obtenidos.")
        # Esperamos 5 segundos entre cada uno para evitar bloqueos
        time.sleep(5)

    # Guardamos todo en un archivo llamado data.json
    with open('data.json', 'w') as f:
        json.dump(datos_finales, f, indent=4)
    
    print("¡Hecho! Los datos se guardaron en data.json")

if __name__ == "__main__":
    ejecutar_app()
