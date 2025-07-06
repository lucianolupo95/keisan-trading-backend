import yfinance as yf
from django.http import JsonResponse
import pandas as pd

def fetch_data(request):
    ticker = request.GET.get("ticker")
    interval = request.GET.get("interval", "1d")
    period = request.GET.get("period", "7d")

    if not ticker:
        return JsonResponse({"error": "ticker is required"}, status=400)

    try:
        df = yf.download(ticker, interval=interval, period=period)

        # 1. Asegurarse de que el índice 'Date' sea una columna
        df.reset_index(inplace=True)

        # 2. Aplanar las columnas si tienen un MultiIndex
        # Esto ocurre si yfinance devuelve algo como ('Close', 'AAPL')
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]
            # O si solo quieres el segundo nivel (el nombre de la métrica como 'Close', 'High')
            # df.columns = [col[1] if isinstance(col, tuple) and col[1] else col[0] for col in df.columns]
            # Si solo te importa el primer nivel (como 'Date', 'Open', 'High', 'Low', 'Close', 'Volume')
            # df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

            # Para tu caso específico con ('Date', '') y ('Close', 'AAPL'),
            # la estrategia de arriba con '_'.join(col).strip() podría dar 'Date_' y 'Close_AAPL'
            # Una alternativa más específica para eliminar el segundo nivel vacío o el ticker:
            new_columns = []
            for col in df.columns:
                if isinstance(col, tuple):
                    if col[1]: # Si el segundo elemento de la tupla no está vacío (ej. 'AAPL')
                        new_columns.append(col[0]) # Solo toma el primer elemento ('Close')
                    else: # Si el segundo elemento está vacío (ej. para 'Date')
                        new_columns.append(col[0]) # Solo toma el primer elemento ('Date')
                else:
                    new_columns.append(col) # Si ya es una cadena simple
            df.columns = new_columns


        # 3. Convertir la columna 'Date' (ahora una string simple) a formato string para JSON
        # Asumiendo que la columna se llama 'Date' después de reset_index y aplanar
        if 'Date' in df.columns:
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

        # 4. Convertir el DataFrame a una lista de diccionarios
        data = df.to_dict(orient="records")

        return JsonResponse({
            "ticker": ticker,
            "interval": interval,
            "period": period,
            "data": data
        })
    except Exception as e:
        # Captura cualquier error en la descarga o procesamiento
        return JsonResponse({"error": str(e)}, status=500)