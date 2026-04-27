from yahooquery import Ticker
import json
import time

# Lista final de activos
activos = ['CSPX.L', 'BTC-USD', 'BAC', 'COPX', 'URNU', 'MSFT', 'PLTR', 'TSM', 'ASTS', 'HIMS', 'ASML', 'CNXC']

def iniciar():
    print("Conectando con Yahoo...")
    try:
        t = Ticker(activos, asynchronous=False)
        
        # Obtenemos los datos
        detalles = t.summary_detail
        precios = t.price
        finanzas = t.financial_data
        
        resultado = []
        
        for ticker in activos:
            d = detalles.get(ticker, {})
            p = precios.get(ticker, {})
            f = finanzas.get(ticker, {})
            
            # Formatear porcentajes de forma segura
            def pct(v):
                return f"{round(v * 100, 2)}%" if isinstance(v, (int, float)) else "N/A"

            resultado.append({
                "ticker": ticker,
                "precio": p.get('regularMarketPrice', 'N/A'),
                "P_E": d.get('trailingPE', 'N/A'),
                "ROE": pct(f.get('returnOnEquity')),
                "Margen_Op": pct(f.get('operatingMargins')),
                "Target": f.get('targetMeanPrice', 'N/A'),
                "Actualizado": time.strftime('%H:%M:%S')
            })
            print(f"OK: {ticker}")
            time.sleep(1)

        with open('data.json', 'w') as f_out:
            json.dump(resultado, f_out, indent=4)
            
    except Exception as e:
        print(f"Fallo: {e}")

if __name__ == "__main__":
    iniciar()
