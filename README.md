## 🎭 Theatre Service 

## Rozehan Oleksii 55666

## Opis: Aplikacja internetowa do zarządzania sprzedażą biletów do teatru, rezerwacją miejsc, oglądaniem spektakli. Obsługuje rejestrację użytkowników, integrację z zewnętrznymi API (Ticketmaster, PayU) oraz interfejs Django + REST API.

## Technologie

Backend: 
 - Python, 
 - Django 5.2

API: 
 - Django REST Framework,
 - drf-spectacular

Frontend: 
 - JavaScript, 
 - HTML/CSS

DB: 
- SQLite

Integracje:
 - Ticketmaster API — do informacji o wydarzeniu
 - PayU API — do płatności online

## Struktura katalogów
teatr_55666/  
├── main_service/# logika biznesowa: spektakle, bilety, rezerwacje   
├── users/ # użytkownicy, logowanie, rejestracja   
├── payu_api/ # integracja z płatnościami PayU  
├── ticketmaster_api/ # integracja z API Ticketmaster  
├── frontend/ # HTML, JS, CSS  
├── teatr_55666/ # konfiguracja Django (settings, urls, wsgi)  
└── db.sqlite3 # baza danych  


## 📦 Używane technologie i biblioteki
 Django REST Framework:
 - rest_framework, 
 - rest_framework.authtoken
 - drf_spectacular 
 - python-decouple
 - django-cors-headers

Moduły projektu:
- main_service
- users
- frontend
- payu_api — integracja z systemem płatności PayU
- ticketmaster_api — połączenie z Ticketmaster

## Wymagania systemowe

- Python 3.10+
- pip
- virtualenv (opcjonalnie)
- dostęp do Internetu (dla integracji z API)

## Start projektu
1)Klonowanie i instalacja
 
 - git clone https://github.com/weuis/teatr_55666.git
 - cd teatr_55666
 - python -m venv venv
 - source venv/bin/activate

2)Stosowanie migracji i uruchamianie serwera

- python manage.py migrate
- python manage.py runserver

3)Dostęp Dokumentacja API: 

- API-dokumentacja: http://localhost:8000/api/schema/swagger-ui/\
- Administrator: http://localhost:8000/admin

## Konfiguracja środowiska (.env)

Utwórz plik `.env` w katalogu głównym i uzupełnij:

PayU

PAYU_CLIENT_ID=...
PAYU_CLIENT_SECRET=...

Ticketmaster

TICKETMASTER_API_KEY=...

## Testowanie

Aby uruchomić testy jednostkowe:
python manage.py test
