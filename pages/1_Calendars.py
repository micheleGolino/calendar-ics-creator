from datetime import datetime
import pytz
import streamlit as st
import string as str

st.set_page_config(page_title="Calendar ICS", layout="wide", page_icon="🗓️")

def create_ics_content(summary, dtstart, dtend, attendees, description, organizer):
    format_string = "%Y%m%dT%H%M%SZ"
    dtstamp = datetime.now(pytz.utc).strftime(format_string)
    dtstart_utc = dtstart.strftime(format_string)
    dtend_utc = dtend.strftime(format_string)

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
    
    if organizer: 
        ics_content += f"ORGANIZER;CN={organizer}:MAILTO:{organizer}\n"

    # Aggiunta degli indirizzi email come partecipanti
    if attendees:
        if ";" in attendees:
            array_attendees = attendees.split(";")
        else:
            array_attendees = [attendees]  # Metti attendees in una lista se non c'è il separatore ";"

        for attendee in array_attendees:
            ics_content += f"ATTENDEE;CN={attendee}:mailto:{attendee}\n"

    ics_content += "END:VEVENT\nEND:VCALENDAR\n"
    return ics_content

def convert_date_in_datetime(date, hours, minutes, seconds):
    timezone = pytz.utc
    return datetime(date.year, date.month, date.day, hours, minutes, seconds, tzinfo=timezone)

def valid_fields(input_title, dtstart, dtstart_hours, dtstart_minutes, dtstart_seconds, dtend, dtend_hours, dtend_minutes, dtend_seconds, attendees):
    if not input_title or not attendees or not dtstart or not dtend:
        return False
    
    if dtstart_hours < 0 or dtstart_hours > 23 or dtend_hours < 0 or dtend_hours > 23:
        return False
    
    if dtstart_minutes < 0 or dtstart_minutes > 59 or dtend_minutes < 0 or dtend_minutes > 59:
        return False

    if dtstart_seconds < 0 or dtstart_seconds > 59 or dtend_seconds < 0 or dtend_seconds > 59:
        return False

    return True

def saving_files(input_title, ics_content):
    if ".ics" in input_title:
        file_name = input_title
    else:
        file_name = f"{input_title}.ics"

    with open(file_name, mode="+wt", encoding="utf8") as file:
        file.write(ics_content)
        st.success(f"File {file_name} creato con successo")


def main():
    now_date = datetime.now()
    curr_hours = now_date.hour
    curr_minutes = now_date.minute 
    curr_seconds = now_date.second
    st.markdown("<h1>Inserisci qui i dati per creare il tuo file calendar .ics</h1>", unsafe_allow_html=True)
    input_title = st.text_input("Inserisci qui il titolo dell'evento (*)", key="input_title")
    input_organizer = st.text_input("Inserisci qui il nome dell'organizzatore", key="input_organizer")
    input_description = st.text_input("Inserisci qui la descrizione dell'evento", key="input_description")
    st.divider()
    st.markdown("<h2>Inserisci la data di inizio</h2>", unsafe_allow_html=True)
    dtstart = st.date_input("Seleziona la data di inizio (*)", "today", key="date_start")
    dtstart_hours = st.number_input("Inserisci l'ora (*)", min_value=0, max_value=23, step=1, key="dtstart_hours", value=curr_hours)
    dtstart_minutes = st.number_input("Inserisci i minuti (*)", min_value=0, max_value=59, step=5, key="dtstart_minutes", value=curr_minutes)
    dtstart_seconds = st.number_input("Inserisci i secondi (*)", min_value=0, max_value=59, step=5, key="dtstart_seconds", value=curr_seconds)
    st.divider()
    st.markdown("<h2>Inserisci la data di fine</h2>", unsafe_allow_html=True)
    dtend = st.date_input("Seleziona la data di fine (*)", "today", key="date_end")
    dtend_hours = st.number_input("Inserisci l'ora (*)", min_value=0, max_value=23, step=1, key="dtend_hours", value=curr_hours)
    dtend_minutes = st.number_input("Inserisci i minuti (*)", min_value=0, max_value=59, step=5, key="dtend_minutes", value=curr_minutes)
    dtend_seconds = st.number_input("Inserisci i secondi (*)", min_value=0, max_value=59, step=5, key="dtend_seconds", value=curr_seconds)
    st.divider()
    attendees = st.text_area("Inserisci le email degli invitati, separati da punto e virgola (;)  (*)", key="text_destinatari")

    if st.button("Crea file calendar .ics", key="button_create_file"):
        if valid_fields(input_title, dtstart, dtstart_hours, dtend_minutes, dtstart_seconds, dtend, dtend_hours, dtend_minutes, dtend_seconds, attendees):
            datestart_to_send = convert_date_in_datetime(dtstart, dtstart_hours, dtstart_minutes, dtstart_seconds)
            dateend_to_send = convert_date_in_datetime(dtend, dtend_hours, dtend_minutes, dtend_seconds)

            # Creazione del contenuto .ics
            ics_content = create_ics_content(input_title, datestart_to_send, dateend_to_send, attendees, input_description, input_organizer)
            saving_files(input_title, ics_content)
        else:
            st.warning("E' necessario compilare prima tutti i campi obbligatori")

main()