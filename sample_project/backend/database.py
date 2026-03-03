# Mock database connection
class Database:
    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True
        return "Connected to DB"

db = Database()
