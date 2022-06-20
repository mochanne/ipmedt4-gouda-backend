<p align="center"><a href="https://laravel.com" target="_blank"><img src="https://raw.githubusercontent.com/laravel/art/master/logo-lockup/5%20SVG/2%20CMYK/1%20Full%20Color/laravel-logolockup-cmyk-red.svg" width="400"></a></p>

# Goude app backend

## Installatie

### Benodigheden:
- PHP
- Composer
- MariaDB
- Python3
- De Python packages in requirements.txt

### Laravel Setup

1. run `composer global require laravel/laravel`
2. maak een MariaDB database aan genaamd `gaudadb`: 
```sql
CREATE DATABASE goudadb;
```
3. maak een MariDB gebruiker aan met als naam `gouda` en wachtwoord `verander_voor_production`:
```sql
CREATE OR REPLACE USER 'gouda'@'localhost' IDENTIFIED BY 'verander_voor_production';
``` 
4. Geef de benodigde privileges aan de gebruiker:
```sql
GRANT ALL PRIVILEGES ON goudadb.* TO 'gouda'@'localhost';
```

⚠️ ***Let op:** Verander deze credentials in production. Dit moet dan ook in het `.env` bestand aangepast worden.* ⚠️

⚠️ ***Let op:** Het `.env` bestand staat **niet** in de `.gitignore`. Voeg deze hieraan toe tijdens productie om te voorkomen dat er legitieme credentials op de git komen* ⚠️


### Data installatie

1. CD naar de root van deze repository (vanaf ./laravel: `cd ..`)

2. Installeer de python packages:
```bash
python3 -m pip install -r requirements.txt
```

3. Download alle route data en volg de installer:
```bash
python3 scraper.py
```

4. Sorteer, vul GPS locaties & verifieer alle route data:
```bash
python3 sorteer.py
```

5. Kopieer de route data naar ./laravel/storage/app/public/: 
```bash
cp -r wandelroutes laravel/storage/app/public/
```

6. CD terug naar deze directory: 
```bash
cd ./laravel
```

7. Link de storage: 
```bash
php artisan storage:link
```

8. Migrate & seed de database met 
```bash
php artisan migrate --seed
```


Het backend is nu klaar voor gebruik.

Herhaal de data installatie stappen om de database informatie te updaten als er veranderingen zijn geweest.