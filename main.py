from yahooquery import Ticker
import json
import time

# Lista actualizada con tus tickers de la imagen + los nuevos
mis_acciones = [
    'CSPX.L', 'BTC-USD', 'BAC', 'COPX', 'URNU', 
    'MSFT', 'PLTR', 'TSM', 'ASTS', 'HIMS', 
    'ASML', 'CNXC'
]

def ejecutar_app():
    print("Iniciando consulta a Yahoo Finance...")
    t = Ticker(mis_acciones)
    
    # Obtenemos datos de resumen y estadísticas clave
    ratios = t.summary_detail
    price_data = t.price
    
    datos_finales = []
    
    for ticker in mis_acciones:
        # Extraemos la información de cada sección
        info = ratios.get(ticker, {})
        p_info = price_data.get(ticker, {})
        
        # Datos que solicitaste y adicionales útiles
        pe = info.get('trailingPE', 'N/A')
        precio_actual = p_info.get('regularMarketPrice', 'N/A')
        cambio_porcentaje = p_info.get('regularMarketChangePercent', 0) * 100
        market_cap = info.get('marketCap', 'N/A')
        
        datos_finales.append({
            "ticker": ticker,
            "precio": precio_actual,
            "cambio_diario_%": round(cambio_porcentaje, 2),
            "pe_ratio": pe,
            "market_cap": market_cap
        })
        print(f"Datos de {ticker} obtenidos.")
        time.sleep(2) # Pausa breve para evitar bloqueos

    with open('data.json', 'w') as f:
        json.dump(datos_finales, f, indent=4)
    
    print("¡Hecho! data.json actualizado.")

if __name__ == "__main__":
    ejecutar_app()
