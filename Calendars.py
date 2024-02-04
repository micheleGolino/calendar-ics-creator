import streamlit as st
import pytz
import io
from datetime import datetime, time
from translations import translations

st.set_page_config(page_title="Calendars ICS", layout="centered", page_icon="🗓️")

option_languages = ["EN", "ES", "IT", "FR", "DE", "PT", "NL"]
sorted_languages = sorted(option_languages)
index_en_language = sorted_languages.index("EN")
language = st.sidebar.selectbox("Select Language", options=sorted_languages, key="select_language", index=index_en_language)
texts = translations[language]

def create_ics_content(summary, dtstart, dtend, attendees, description, organizer):
    """
    Creates the content of an ICS file for a calendar event.

    Parameters:
    summary (str): The summary or title of the event.
    dtstart (datetime): The start date and time of the event in UTC.
    dtend (datetime): The end date and time of the event in UTC.
    attendees (str): A string of email addresses of attendees, separated by semicolons.
    description (str): The description of the event.
    organizer (str): The email address of the organizer.

    Returns:
    str: A string representing the content of the ICS file.
    """
    format_string = "%Y%m%dT%H%M%SZ"
    dtstamp = datetime.now(pytz.utc).strftime(format_string)
    dtstart_utc = dtstart.strftime(format_string)
    dtend_utc = dtend.strftime(format_string)

    ics_content = (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "PRODID:-//github.com//micheleGolino//NONSGML v1.0//EN\n"
        "BEGIN:VEVENT\n"
        f"UID:{dtstamp}/github.com/micheleGolino\n"
        f"DTSTAMP:{dtstamp}\n"
        f"DTSTART:{dtstart_utc}\n"
        f"DTEND:{dtend_utc}\n"
        f"SUMMARY:{summary}\n"
    )
    
    if organizer: 
        ics_content += f"ORGANIZER;CN={organizer}:MAILTO:{organizer}\n"

    if attendees:
        attendees_list = attendees.split(";") if ";" in attendees else [attendees]
        for attendee in attendees_list:
            ics_content += f"ATTENDEE;CN={attendee}:mailto:{attendee}\n"

    if description:
        ics_content += f"DESCRIPTION:{description}\n"
            
    ics_content += "END:VEVENT\nEND:VCALENDAR\n"
    return ics_content

def convert_date_to_datetime(date, hours, minutes, seconds):
    """
    Converts a date and time into a datetime object in UTC.

    Parameters:
    date (date): The date.
    hours (int): The hour of the day.
    minutes (int): The minutes of the hour.
    seconds (int): The seconds of the minute.

    Returns:
    datetime: A datetime object representing the specified date and time in UTC.
    """
    timezone = pytz.utc
    return datetime(date.year, date.month, date.day, hours, minutes, seconds, tzinfo=timezone)

def validate_fields(input_title, dtstart, dtstart_hours, dtstart_minutes, dtstart_seconds, dtend, dtend_hours, dtend_minutes, dtend_seconds, attendees):
    """
    Validates the input fields for creating an ICS file.

    Parameters:
    input_title (str): The title of the event.
    dtstart (date): The start date of the event.
    dtstart_hours, dtstart_minutes, dtstart_seconds (int): The time components of the start date.
    dtend (date): The end date of the event.
    dtend_hours, dtend_minutes, dtend_seconds (int): The time components of the end date.
    attendees (str): The string of attendees' email addresses.

    Returns:
    bool: True if all fields are valid, False otherwise.
    """
    if not input_title or not attendees or not dtstart or not dtend:
        return False
    if any(hour < 0 or hour > 23 for hour in [dtstart_hours, dtend_hours]):
        return False
    if any(minute < 0 or minute > 59 for minute in [dtstart_minutes, dtend_minutes]):
        return False
    if any(second < 0 or second > 59 for second in [dtstart_seconds, dtend_seconds]):
        return False
    
    start_datetime = datetime.combine(dtstart, time(dtstart_hours, dtstart_minutes, dtstart_seconds))
    end_datetime = datetime.combine(dtend, time(dtend_hours, dtend_minutes, dtend_seconds))

    if end_datetime < start_datetime:
        return False

    return True

def save_files(input_title, ics_content):
    """
    Saves the ICS content to a file.

    Parameters:
    input_title (str): The title of the event, used as the file name.
    ics_content (str): The content of the ICS file.

    Side Effect:
    Writes the ICS content to a file named '<input_title>.ics' or uses the input_title as the filename if it ends with '.ics'.
    """
    file_name = f"{input_title}.ics" if ".ics" not in input_title else input_title
    with open(file_name, mode="+wt", encoding="utf8") as file:
        file.write(ics_content)
        st.success(f"File {file_name} created successfully")

    import io

def download_ics_file(input_title, ics_content):
    """
    Provides a download button for the ICS file.

    Parameters:
    input_title (str): The title of the event, used as the file name.
    ics_content (str): The content of the ICS file.

    Side Effect:
    Provides a button in the Streamlit interface to download the ICS content as a file.
    """
    file_name = f"{input_title}.ics" if ".ics" not in input_title else input_title
    # Create a buffer to hold the file content
    buffer = io.BytesIO()
    buffer.write(ics_content.encode('utf-8')) 
    buffer.seek(0)
    # Provide a download button
    st.download_button(
        label=texts["download_button_label"],
        data=buffer,
        file_name=file_name,
        mime="text/calendar"
    )



def get_current_time():
    """
    Gets the current time.

    Returns:
    tuple: A tuple containing the current hour and minute.
    """
    now_date = datetime.now()
    return now_date.hour, now_date.minute

def input_event_details():
    """
    Captures the event details from the user using Streamlit input fields.

    Returns:
    tuple: A tuple containing the event title, organizer, and description input by the user.
    """
    input_title = st.text_input(texts["event_title_input"], key="input_title")
    input_organizer = st.text_input(texts["organizer_input"], key="input_organizer")
    input_description = st.text_input(texts["description_input"], key="input_description")
    return input_title, input_organizer, input_description

def input_date_details(prefix, current_hour, current_minute):
    """
    Captures the date and time details for either start or end of the event.

    Parameters:
    prefix (str): The prefix indicating whether it's for start or end date.
    current_hour (int): The current hour to set as default.
    current_minute (int): The current minute to set as default.

    Returns:
    tuple: A tuple containing the selected date, hour, minute, and second.
    """
    st.markdown(texts[f"{prefix}_date_section"], unsafe_allow_html=True)
    date = st.date_input(texts[f"{prefix}_date_select"], "today", key=f"{prefix}_date")
    hour = st.number_input(texts["hours_input"], min_value=0, max_value=23, step=1, key=f"{prefix}_hours", value=current_hour)
    minute = st.number_input(texts["minutes_input"], min_value=0, max_value=59, step=5, key=f"{prefix}_minutes", value=current_minute)
    second = st.number_input(texts["seconds_input"], min_value=0, max_value=59, step=5, key=f"{prefix}_seconds")
    return date, hour, minute, second

def main():
    """
    The main function of the Streamlit app. It creates an interface for the user to input event details and generates an ICS file.
    """
    st.sidebar.markdown(texts["sidebar_text"], unsafe_allow_html=True)

    curr_hours, curr_minutes = get_current_time()
    st.markdown(texts["main_title_page"], unsafe_allow_html=True)

    input_title, input_organizer, input_description = input_event_details()

    st.divider()
    dtstart, dtstart_hours, dtstart_minutes, dtstart_seconds = input_date_details("start", curr_hours, curr_minutes)

    st.divider()
    dtend, dtend_hours, dtend_minutes, dtend_seconds = input_date_details("end", curr_hours, curr_minutes)

    st.divider()
    attendees = st.text_area(texts["invitees_input"], key="text_attendees")

    if st.button(texts["check_validate_button"], key="button_validate_fields"):
        if validate_fields(input_title, dtstart, dtstart_hours, dtend_minutes, dtstart_seconds, dtend, dtend_hours, dtend_minutes, dtend_seconds, attendees):
            datestart_to_send = convert_date_to_datetime(dtstart, dtstart_hours, dtstart_minutes, dtstart_seconds)
            dateend_to_send = convert_date_to_datetime(dtend, dtend_hours, dtend_minutes, dtend_seconds)
            ics_content = create_ics_content(input_title, datestart_to_send, dateend_to_send, attendees, input_description, input_organizer)
            st.success(texts["validation_success"])
            download_ics_file(input_title, ics_content)
        else:
            st.warning(texts["validation_warning"])


main()
