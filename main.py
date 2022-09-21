import asyncio, aiohttp, time, os

apiKey = os.getenv ('ALPHAVANTAGE_API_KEY')
url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=5min&apikey={}"
empresas = ['AAPL', 'GOOG', 'TSLA', 'MSFT', 'AAPL','AAPL', 'GOOG', 'TSLA', 'MSFT', 'AAPL','AAPL', 'GOOG', 'TSLA', 'MSFT', 'AAPL']
datos = []

inicio = time.time ()

def getRequests (sesion) -> list:
    peticiones = []

    for empresa in empresas:
        peticiones.append(asyncio.create_task (sesion.get (url.format (empresa, apiKey), ssl=False)))

    return peticiones

async def request () -> None:
    #Usando una funcion asincrona, no necesitamos esperar a que termine el proceso para avanzar.
    #La clausula with permite cerrar la sesion automaticamente y prevenir que se ejecute el codigo en caso de que no se abra.
    async with aiohttp.ClientSession () as sesion:
        peticiones = getRequests (sesion)
        respuestas = await asyncio.gather (*peticiones)

        for respuesta in respuestas:
            datos.append (await respuesta.json ())        

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run (request ())

fin = time.time ()
tiempoTotal = fin - inicio

print (f"Tomo {tiempoTotal} segundos realizar {len (empresas)} consultas a la API.")
print (datos)

