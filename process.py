import random

class Process:
    def __init__(self, process_id, num_pages):
        self.process_id = process_id
        self.num_pages = num_pages
        self.pages = [random.randint(0, 9) for _ in range(num_pages)]  # Simulating pages 0-9
