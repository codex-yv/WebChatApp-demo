from datetime import datetime
import pytz
def ISTtime():
    ist = pytz.timezone('Asia/Kolkata')
    ist_time = datetime.now(ist)
    return ist_time.strftime("%I:%M %p")