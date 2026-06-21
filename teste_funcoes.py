from datetime import datetime

data_teste = datetime(2026, 12, 21).date()

hoje = datetime.today().date()

if data_teste < hoje:
    print(f" MANUTENÇÃO ATRASADA! venceu em: {data_teste.strftime('%d/%m/%Y')}")
else:
    if data_teste == hoje:
        print(f"Manutenção programada para hoje")
    else:
        print(f" Próxima em manutenção:{data_teste.strftime('%d/%m/%Y')}")