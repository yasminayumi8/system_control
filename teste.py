from datetime import datetime

data = ['25/12/2024', '30/11/2023', '20/10/2024']
print("Original:", data)

# Convertendo strings para objetos datetime
datas_ordenadas = sorted(data, key=lambda x: datetime.strptime(x, '%d/%m/%Y'))

print("Ordenada:", datas_ordenadas)