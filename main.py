from yahooquery import Ticker
import json
import time

# Tu lista completa de seguimiento
mis_activos = [
    'CSPX.L', 'BTC-USD', 'BAC', 'COPX', 'URNU', 
    'MSFT', 'PLTR', 'TSM', 'ASTS', 'HIMS', 
    'ASML', 'CNXC'
]

def ejecutar_analisis():
    print("Iniciando escaneo de mercado...")
    t = Ticker(mis_activos)
    
    # Extraemos los módulos necesarios
    # summary_detail: P/E Ratio, Market Cap
    # financial_data: Target Price (Precio objetivo)
    # price: Precios actuales y nombres
    summary = t.summary_detail
    financials = t.financial_data
    price_data = t.price
    
    datos_finales = []
    
    for ticker in mis_activos:
        s_info = summary.get(ticker, {})
        f_info = financials.get(ticker, {})
        p_info = price_data.get(ticker, {})
        
        # Procesamos la información
        datos_finales.append({
            "ticker": ticker,
            "nombre": p_info.get('shortName', ticker),
            "precio_actual": p_info.get('regularMarketPrice', 'N/A'),
            # Datos de origen trimestral:
            "pe_ratio": s_info.get('trailingPE', 'N/A'),
            "market_cap": s_info.get('marketCap', 'N/A'),
            # Datos de analistas:
            "target_price": f_info.get('targetMeanPrice', 'N/A'),
            "fecha_revision": time.strftime('%Y-%m-%d')
        })
        
        print(f"Sincronizando {ticker}...")
        # Pausa de seguridad para evitar bloqueos de IP en GitHub
        time.sleep(2)

    # Guardamos el resultado
    with open('data.json', 'w') as f:
        json.dump(datos_finales, f, indent=4)
    
    print("¡Éxito! Archivo data.json actualizado.")

if __name__ == "__main__":
    ejecutar_analisis()
