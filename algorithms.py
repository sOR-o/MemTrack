from collections import deque

class FIFO:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.page_queue = deque()

    def access_page(self, process_id, page_id):
        if page_id in self.memory_manager.memory:
            print(f"Page {page_id} already in memory.")
            return
        else:
            self.handle_page_fault(page_id)

    def handle_page_fault(self, page_id):
        if len(self.page_queue) < self.memory_manager.memory_size:
            frame = self.memory_manager.add_page_to_memory(page_id)
            self.page_queue.append(page_id)
            print(f"Loaded page {page_id} into memory at frame {frame}.")
        else:
            old_page = self.page_queue.popleft()
            self.memory_manager.remove_page_from_memory(old_page)
            self.page_queue.append(page_id)
            frame = self.memory_manager.add_page_to_memory(page_id)
            print(f"Page {old_page} replaced with page {page_id} at frame {frame}.")

class LRU:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.page_stack = []

    def access_page(self, process_id, page_id):
        if page_id in self.memory_manager.memory:
            print(f"Page {page_id} already in memory.")
            self.page_stack.remove(page_id)
            self.page_stack.append(page_id)
        else:
            self.handle_page_fault(page_id)

    def handle_page_fault(self, page_id):
        if len(self.page_stack) < self.memory_manager.memory_size:
            frame = self.memory_manager.add_page_to_memory(page_id)
            self.page_stack.append(page_id)
            print(f"Loaded page {page_id} into memory at frame {frame}.")
        else:
            old_page = self.page_stack.pop(0)
            self.memory_manager.remove_page_from_memory(old_page)
            self.page_stack.append(page_id)
            frame = self.memory_manager.add_page_to_memory(page_id)
            print(f"Page {old_page} replaced with page {page_id} at frame {frame}.")
