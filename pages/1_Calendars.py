from datetime import datetime
import pytz
import streamlit as st


st.set_page_config(page_title="Calendar ICS", layout="wide", page_icon="🗓️")

# Funzione per creare il contenuto di un file .ics
def create_ics_content(summary, dtstart, dtend, attendees):
    # Formattazione delle date in formato UTC
    dtstamp = datetime.now(pytz.utc).strftime("%Y%m%dT%H%M%SZ")
    dtstart_utc = dtstart.strftime("%Y%m%dT%H%M%SZ")
    dtend_utc = dtend.strftime("%Y%m%dT%H%M%SZ")

    # Creazione del contenuto del file .ics
    ics_content = (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "PRODID:-//chat.openai.com//NONSGML v1.0//EN\n"
        "BEGIN:VEVENT\n"
        f"UID:{dtstamp}/chat.openai.com\n"
        f"DTSTAMP:{dtstamp}\n"
        f"DTSTART:{dtstart_utc}\n"
        f"DTEND:{dtend_utc}\n"
        f"SUMMARY:{summary}\n"
    )
    
    # Aggiunta degli indirizzi email come partecipanti
    for attendee in attendees:
        ics_content += f"ATTENDEE;CN={attendee}:mailto:{attendee}\n"

    ics_content += "END:VEVENT\nEND:VCALENDAR\n"
    return ics_content

# Dettagli dell'evento
st.markdown("<h1>Inserisci qui i dati per creare il tuo file calendar .ics</h1>", unsafe_allow_html=True)
input_title = st.text_input("Inserisci qui il titolo dell'evento", key="input_title")
input_description = st.text_input("Inserisci qui la descrizione dell'evento", key="input_description")
st.divider()
st.markdown("<h2>Inserisci la data di inizio</h2>", unsafe_allow_html=True)
dtstart = st.date_input("Seleziona la data di inizio", "today", key="date_start")
dtstart_hours = st.number_input("Inserisci l'ora", min_value=0, max_value=23, step=1, key="dtstart_hours")
dtstart_minutes = st.number_input("Inserisci i minuti", min_value=0, max_value=59, step=1, key="dtstart_minutes")
dtstart_seconds = st.number_input("Inserisci i secondi", min_value=0, max_value=59, step=1, key="dtstart_seconds")
st.divider()
st.markdown("<h2>Inserisci la data di fine</h2>", unsafe_allow_html=True)
dtend = st.date_input("Seleziona la data di fine", "today", key="date_end")
dtend_hours = st.number_input("Inserisci l'ora", min_value=0, max_value=23, step=1, key="dtend_hours")
dtend_minutes = st.number_input("Inserisci i minuti", min_value=0, max_value=59, step=1, key="dtend_minutes")
dtend_seconds = st.number_input("Inserisci i secondi", min_value=0, max_value=59, step=1, key="dtend_seconds")
st.divider()
attendees = st.text_area("Inserisci le email degli invitati", key="text_destinatari")

# Converti la data in datetime

datestart_to_send = datetime(dtstart.year, dtstart.month, dtstart.day, 10, 0, 0, tzinfo=pytz.utc)
dateend_to_send = datetime(2029, 10, 13, 12, 0, 0, tzinfo=pytz.utc)  # Durata di 2 ore
attendees = ["michelegolino94@gmail.com", "pepeangela12@gmail.com"]

# Creazione del contenuto .ics
ics_content = create_ics_content(input_title, datestart_to_send, dateend_to_send, attendees)

# Salvataggio del file .ics
file_path = '/mnt/data/matrimonio_golino_pepe.ics'
with open(file_path, 'w') as f:
    f.write(ics_content)

file_path
