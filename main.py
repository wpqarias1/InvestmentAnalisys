from yahooquery import Ticker
import json
import time

mis_activos = [
    'CSPX.L', 'BTC-USD', 'BAC', 'COPX', 'URNU', 
    'MSFT', 'PLTR', 'TSM', 'ASTS', 'HIMS', 
    'ASML', 'CNXC'
]

def ejecutar_app():
    print("Iniciando escaneo detallado...")
    t = Ticker(mis_activos)
    
    # Módulos necesarios para las nuevas métricas
    summary = t.summary_detail
    financials = t.financial_data
    key_stats = t.key_stats
    
    datos_finales = []
    
    for ticker in mis_activos:
        print(f"Obteniendo métricas de {ticker}...")
        
        # Obtenemos diccionarios de datos (o vacíos si fallan)
        s = summary.get(ticker, {}) if isinstance(summary, dict) else {}
        f = financials.get(ticker, {}) if isinstance(financials, dict) else {}
        k = key_stats.get(ticker, {}) if isinstance(key_stats, dict) else {}
        
        # Función auxiliar para redondear porcentajes de forma segura
        def fmt_pct(valor):
            return f"{round(valor * 100, 2)}%" if isinstance(valor, (int, float)) else "N/A"

        # Construcción del reporte con tus nuevas métricas
        datos_finales.append({
            "ticker": ticker,
            "precio": s.get('previousClose', 'N/A'),
            # Métricas de Rentabilidad (Imagen 1)
            "ROE": fmt_pct(f.get('returnOnEquity')),
            "ROIC": fmt_pct(f.get('returnOnAssets')), # Estimado vía ROA
            "Margen_Operativo": fmt_pct(f.get('operatingMargins')),
            "Margen_Neto": fmt_pct(f.get('profitMargins')),
            # Métricas de Deuda y Riesgo (Imagen 2)
            "Current_Ratio": s.get('currentRatio', 'N/A'),
            "Beta": s.get('beta', 'N/A'),
            "P_E_Ratio": s.get('trailingPE', 'N/A'),
            "EPS_Diluido": k.get('trailingEps', 'N/A'),
            "FCF": f.get('freeCashflow', 'N/A'),
            "fecha": time.strftime('%Y-%m-%d')
        })
        
        time.sleep(2) # Pausa para evitar bloqueos

    with open('data.json', 'w') as archivo:
        json.dump(datos_finales, archivo, indent=4)
    
    print("Proceso terminado exitosamente.")

if __name__ == "__main__":
    try:
        ejecutar_app()
    except Exception as e:
        print(f"Error crítico: {e}")
