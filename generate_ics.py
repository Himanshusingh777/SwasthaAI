import os

def create_ics_file(name, reminder_type, reason, date):
    from icalendar import Calendar, Event
    from datetime import datetime, timedelta

    cal = Calendar()
    event = Event()

    start = datetime.strptime(date, "%Y-%m-%d")
    end = start + timedelta(hours=1)

    event.add('summary', f'{reminder_type} - {reason}')
    event.add('dtstart', start)
    event.add('dtend', end)
    event.add('description', f'Reminder for {name}')
    event.add('location', 'SwasthaAI')
    cal.add_component(event)

    # Ensure the 'static' folder exists
    os.makedirs("static", exist_ok=True)

    filename = f"reminder_{name.replace(' ', '_')}_{date}.ics"
    filepath = f"static/{filename}"

    with open(filepath, 'wb') as f:
        f.write(cal.to_ical())

    return filename
