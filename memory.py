class MemoryManagement:
    def __init__(self, memory_size, page_size):
        self.memory_size = memory_size
        self.page_size = page_size
        self.memory = [-1] * memory_size  # -1 means empty (no page)
        self.page_table = {}

    def add_page_to_memory(self, page_id):
        for i in range(self.memory_size):
            if self.memory[i] == -1:
                self.memory[i] = page_id
                return i
        return None  # Memory full, need replacement

    def remove_page_from_memory(self, page_id):
        for i in range(self.memory_size):
            if self.memory[i] == page_id:
                self.memory[i] = -1
                return i
        return None  # Page not found in memory

    def print_memory_status(self):
        print("\nCurrent Memory State:")
        print(self.memory)

    def get_empty_frame(self):
        for i in range(self.memory_size):
            if self.memory[i] == -1:
                return i
        return None

    def get_memory_utilization(self):
        used_memory = sum(1 for frame in self.memory if frame != -1)
        return (used_memory / self.memory_size) * 100

    def print_memory_utilization(self):
        utilization = self.get_memory_utilization()
        print(f"\nMemory Utilization: {utilization:.2f}%")
