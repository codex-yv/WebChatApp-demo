from datetime import datetime
import pytz

def get_last_seen():
    timezone = pytz.timezone('Asia/Kolkata')

    now = datetime.now(timezone)

    formatted_time = now.strftime("last seen %d %b %a %I:%M %p")

    return formatted_time
