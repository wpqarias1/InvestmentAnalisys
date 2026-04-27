from yahooquery import Ticker
import json
import time

# Lista completa de tus activos
mis_activos = [
    'CSPX.L', 'BTC-USD', 'BAC', 'COPX', 'URNU', 
    'MSFT', 'PLTR', 'TSM', 'ASTS', 'HIMS', 
    'ASML', 'CNXC'
]

def ejecutar_app():
    print("Iniciando escaneo de métricas fundamentales...")
    t = Ticker(mis_activos)
    
    # Módulos de datos necesarios
    summary = t.summary_detail
    financials = t.financial_data
    price_data = t.price
    
    datos_finales = []
    
    for ticker in mis_activos:
        print(f"Procesando {ticker}...")
        
        # Obtenemos diccionarios seguros
        s = summary.get(ticker, {}) if isinstance(summary, dict) else {}
        f = financials.get(ticker, {}) if isinstance(financials, dict) else {}
        p = price_data.get(ticker, {}) if isinstance(price_data, dict) else {}

        # Función para convertir decimales a porcentaje (ej: 0.15 -> 15.0%)
        def a_pct(val):
            if isinstance(val, (int, float)):
                return f"{round(val * 100, 2)}%"
            return "N/A"

        # Construimos el diccionario con las métricas de tus imágenes
        reporte = {
            "ticker": ticker,
            "nombre": p.get('shortName', ticker),
            "precio": p.get('regularMarketPrice', 'N/A'),
            "P_E_Ratio": s.get('trailingPE', 'N/A'),
            "ROE": a_pct(f.get('returnOnEquity')),
            "ROIC_estimado": a_pct(f.get('returnOnAssets')), # ROA como aproximación
            "Margen_Operativo": a_pct(f.get('operatingMargins')),
            "Margen_Neto": a_pct(f.get('profitMargins')),
            "Target_Price": f.get('targetMeanPrice', 'N/A'),
            "Beta": s.get('beta', 'N/A'),
            "Actualizado": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        datos_finales.append(reporte)
        time.sleep(2) # Pausa para no ser bloqueado

    # Guardar resultados
    with open('data.json', 'w') as f_out:
        json.dump(datos_finales, f_out, indent=4)
    
    print("¡Proceso completado con éxito!")

if __name__ == "__main__":
    ejecutar_app()
