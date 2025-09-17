from zeep import Client

# URL do WSDL do container rodando localmente
wsdl = "http://localhost:8000/?wsdl"

client = Client(wsdl=wsdl)

# Teste de busca
result = client.service.search_news("npm")

print("🔎 Resultados da busca:")
for r in result:
    print("-", r)