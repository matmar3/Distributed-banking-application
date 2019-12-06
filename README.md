# KIV/DS - Semestrální práce 1
  
## OpenAPI  
Specifikace jednotlivých serverů jsou dostupné na jednotlivých serverech na adrese `http://server/apidocs/` pro dokumentaci a `http://server/spec` pro JSON specifikaci.  

Případně jsou také dostupné na následujících odkazech:
- Sequencer OpenAPI: https://app.swaggerhub.com/apis/School-stuff/DS_SP1_Sequencer/1.0.0
- Shuffler OpenAPI: https://app.swaggerhub.com/apis/School-stuff/DS_SP1_Shuffler/1.0.0
- BankServer OpenAPI: https://app.swaggerhub.com/apis/School-stuff/DS_SP1_BankServer/1.0.0
  
## Spuštění  
  
Pro spuštění serverů je potřeba použít příkaz `vagrant up` v kořenovém adresáři repozitáře. Servery si sami stáhnou vše potřebné pro běh a spustí skript `server.py`, který se nachází v adresáři každého serveru.
  
Klientský program je umístěn v aresáři `client/` a je napsán v jazyce **Python 3**. Pro jeho spuštění bude potřeba doinstalovat balíček **requests** (napříkald příkazem `pip install requests`). Poté je možné spustit klientskou aplikaci následovným způsobem:  
- `python3 client.py -h` - zobrazí nápovědu programu  
- `python3 client.py -at 10` - v tomto módu klient sám zašle 10 náhodně generovaných operací  
- `python3 client.py -d 30000` - v tomto módu klient zašle operaci DEBIT s částkou 30000, podobně by tomu bylo s přepínačem `-c` pro operaci CREDIT  
- `python3 client.py -b` - poslední mód slouží pro vypsání zůstatku na všechn bankovních serverech  
  
V souboru `client/endpoints.cfg` jsou definovány konfigurace jednotlivý serverů a jejich routovací cesty. Soubor slouží pouze jako informace pro klientskou aplikaci, nikoliv pro nastavení serverů.
