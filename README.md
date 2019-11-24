# KIV/DS - Semestrální práce 1

Pro spuštění serverů je potřeba použít příkaz `vagrant up`. Servery si sami stáhnou vše potřebné pro běh a spustí skript `server.py`, který se nachází v adresáři každého serveru.

Klientský program je umístěn v aresáři `client/` a je napsán v jazyce **Python 2**. Pro jeho spuštění bude potřeba doinstalovat balíček **requests** (napříkald příkazem `pip install requests`). Poté je možné spustit klientskou aplikaci následovným způsobem:
- `python client.py -h` - zobrazí nápovědu programu
- `python client.py -at 10` - v tomto módu klient sám zašle 10 náhodně generovaných operací
- `python client.py -d 30000` - v tomto módu klient zašle operaci DEBIT s částkou 30000, podobně by tomu bylo s přepínačem `-c` pro operaci CREDIT
- `python client.py -b` - poslední mód slouží pro vypsání zůstatku na všechn bankovních serverech
V souboru `client/endpoints.cfg` jsou definovány konfigurace jednotlivý serverů a jejich routovací cesty. Soubor slouží pouze jako informace pro klientskou aplikaci, nikoliv pro nastavení serverů.