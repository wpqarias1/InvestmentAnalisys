from yahooquery import Ticker
import json
import time

# Tu lista completa de activos corregida
mis_activos = [
    'CSPX.L', 'BTC-USD', 'BAC', 'COPX', 'URNU', 
    'MSFT', 'PLTR', 'TSM', 'ASTS', 'HIMS', 
    'ASML', 'CNXC'
]

def ejecutar_app():
    print("Iniciando escaneo completo...")
    t = Ticker(mis_activos)
    
    # Módulos de Yahoo para capturar ROE, Márgenes y Target Price
    summary = t.summary_detail
    financials = t.financial_data
    key_stats = t.key_stats
    price_data = t.price
    
    datos_finales = []
    
    for ticker in mis_activos:
        # Extraemos diccionarios de cada sección
        s = summary.get(ticker, {})
        f = financials.get(ticker, {})
        k = key_stats.get(ticker, {})
        p = price_data.get(ticker, {})
        
        # Función para dar formato a porcentajes de forma segura
        def fmt_pct(val):
            return f"{round(val * 100, 2)}%" if isinstance(val, (int, float)) else "N/A"

        datos_finales.append({
            "Ticker": ticker,
            "Nombre": p.get('shortName', ticker),
            "Precio_Actual": p.get('regularMarketPrice', 'N/A'),
            "P_E_Ratio": s.get('trailingPE', 'N/A'),
            "ROE": fmt_pct(f.get('returnOnEquity')),
            "ROIC": fmt_pct(f.get('returnOnAssets')), # Estimado como ROA en Yahoo
            "Margen_Operativo": fmt_pct(f.get('operatingMargins')),
            "Margen_Neto": fmt_pct(f.get('profitMargins')),
            "Target_Price": f.get('targetMeanPrice', 'N/A'),
            "Beta": s.get('beta', 'N/A'),
            "EPS_Diluido": k.get('trailingEps', 'N/A'),
            "Fecha_Analisis": time.strftime('%Y-%m-%d')
        })
        
        print(f"Sincronizando {ticker}...")
        time.sleep(3) # Seguridad anti-bloqueo

    with open('data.json', 'w') as archivo:
        json.dump(datos_finales, archivo, indent=4)
    
    print("Archivo data.json generado con éxito.")

if __name__ == "__main__":
    ejecutar_app()
