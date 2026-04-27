from yahooquery import Ticker
import json
import time
import requests

# Tu lista de activos
mis_activos = [
    'CSPX.L', 'BTC-USD', 'BAC', 'COPX', 'URNU', 
    'MSFT', 'PLTR', 'TSM', 'ASTS', 'HIMS', 
    'ASML', 'CNXC'
]

def ejecutar_app():
    print("Iniciando conexión segura...")
    
    # Creamos una sesión que simula un navegador real
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })

    # Pasamos la sesión a Ticker
    t = Ticker(mis_activos, session=session)
    
    print("Capturando módulos de Yahoo...")
    summary = t.summary_detail
    financials = t.financial_data
    price_data = t.price
    
    datos_finales = []
    
    for ticker in mis_activos:
        print(f"Analizando {ticker}...")
        
        # Validación de datos para evitar que el código se rompa
        s = summary.get(ticker, {}) if isinstance(summary, dict) else {}
        f = financials.get(ticker, {}) if isinstance(financials, dict) else {}
        p = price_data.get(ticker, {}) if isinstance(price_data, dict) else {}

        def a_pct(val):
            if isinstance(val, (int, float)):
                return f"{round(val * 100, 2)}%"
            return "N/A"

        reporte = {
            "ticker": ticker,
            "nombre": p.get('shortName', ticker),
            "precio": p.get('regularMarketPrice', 'N/A'),
            "P_E_Ratio": s.get('trailingPE', 'N/A'),
            "ROE": a_pct(f.get('returnOnEquity')),
            "Margen_Operativo": a_pct(f.get('operatingMargins')),
            "Target_Price": f.get('targetMeanPrice', 'N/A'),
            "Beta": s.get('beta', 'N/A'),
            "Actualizado": time.strftime('%Y-%m-%d %H:%M')
        }
        
        datos_finales.append(reporte)
        # Pausa obligatoria de 3 segundos entre activos
        time.sleep(3)

    with open('data.json', 'w') as f_out:
        json.dump(datos_finales, f_out, indent=4)
    
    print("¡Éxito! El archivo data.json ha sido actualizado.")

if __name__ == "__main__":
    try:
        ejecutar_app()
    except Exception as e:
        print(f"Error detectado: {e}")
