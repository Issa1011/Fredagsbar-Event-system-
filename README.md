# Fredagsbarens event-system
Et simpelt system til at oprette og administrere events til fredagsbaren.

### Teknologier
- Python
- Flask (API)
- Streamlit (Hjemmeside)
- httpx
- Docker

### Funktioner
- Se alle events og ledige pladser
- Opret nye events
- Tilmeld og afmeld deltagere
- Slet events
- Vis fejlbeskeder, hvis APIén ikke svarer

### Sådan starter du projektet
Åbn en terminal i projektmappen, og kør:
docker compose up --build

Åben derefter hjemmesiden på http://localhost:8501.

APIén kan tilgåes på http://localhost:5001/events.

### Bemærkninger
Events gemmes i hukommelsen og nulstilles, når Flask genstartes.
