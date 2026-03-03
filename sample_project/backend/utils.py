import datetime

def format_date(date_obj):
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")

def generate_id():
    import uuid
    return str(uuid.uuid4())
