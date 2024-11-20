import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from memory import MemoryManagement
from algorithms import FIFO, LRU
from process import Process

class MemoryManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Simulator")
        self.root.geometry("600x600")

        # Set up frames
        self.setup_controls_frame()
        self.setup_output_frame()

    def setup_controls_frame(self):
        """Create the controls section for the UI"""
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(pady=20)

        # Number of frames
        self.frames_label = tk.Label(self.controls_frame, text="Number of Frames:")
        self.frames_label.grid(row=0, column=0, padx=10)

        self.frames_entry = tk.Entry(self.controls_frame)
        self.frames_entry.grid(row=0, column=1)

        # Algorithm selection
        self.algorithm_label = tk.Label(self.controls_frame, text="Choose Algorithm:")
        self.algorithm_label.grid(row=1, column=0, padx=10)

        self.algorithm_var = tk.StringVar(value="FIFO")
        self.algorithm_fifobtn = tk.Radiobutton(self.controls_frame, text="FIFO", variable=self.algorithm_var, value="FIFO")
        self.algorithm_lrubtn = tk.Radiobutton(self.controls_frame, text="LRU", variable=self.algorithm_var, value="LRU")
        self.algorithm_fifobtn.grid(row=1, column=1)
        self.algorithm_lrubtn.grid(row=1, column=2)

        # Start simulation button
        self.start_button = tk.Button(self.controls_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=2, column=1, pady=10)

    def setup_output_frame(self):
        """Set up the frame to show simulation output"""
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(pady=20)

        # Output display
        self.output_label = tk.Label(self.output_frame, text="Memory State & Page Faults")
        self.output_label.grid(row=0, column=0, padx=10)

        self.output_text = tk.Text(self.output_frame, width=40, height=10)
        self.output_text.grid(row=1, column=0, padx=10, pady=10)

        # Canvas for Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, self.output_frame)
        self.canvas.get_tk_widget().grid(row=2, column=0, pady=10)

    def start_simulation(self):
        """Start the memory management simulation"""
        try:
            num_frames = int(self.frames_entry.get())
            if num_frames <= 0:
                raise ValueError("Number of frames must be a positive integer.")
            
            # Generate processes and simulate memory management
            processes = [Process(i, random.sample(range(10), 5)) for i in range(3)]
            memory_management = MemoryManagement(num_frames)

            # Choose the page replacement algorithm
            algorithm = self.algorithm_var.get()
            if algorithm == "FIFO":
                page_replacement_algorithm = FIFO(memory_management)
            elif algorithm == "LRU":
                page_replacement_algorithm = LRU(memory_management)
            else:
                raise ValueError("Invalid algorithm selected.")

            # Run the simulation and collect output data
            memory_state = []
            page_faults = []
            memory_utilization = []

            for process in processes:
                for page in process.pages:
                    memory_state.append(memory_management.memory)
                    page_faults.append(memory_management.page_faults)
                    memory_utilization.append(memory_management.get_memory_utilization())
                    memory_management.access_page(page, page_replacement_algorithm)
            
            # Display the results
            self.display_results(memory_state, page_faults, memory_utilization)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_results(self, memory_state, page_faults, memory_utilization):
        """Display the simulation results in the output section"""
        self.output_text.delete(1.0, tk.END)

        # Show memory state and page faults
        for i in range(len(memory_state)):
            self.output_text.insert(tk.END, f"Memory: {memory_state[i]} | Page Faults: {page_faults[i]}\n")

        # Plot memory utilization graph
        self.ax.clear()
        self.ax.plot(memory_utilization, label='Memory Utilization (%)')
        self.ax.set_title("Memory Utilization Over Time")
        self.ax.set_xlabel("Time (steps)")
        self.ax.set_ylabel("Utilization (%)")
        self.ax.legend()
        self.canvas.draw()

# Initialize Tkinter root window
root = tk.Tk()

# Create the memory management GUI
app = MemoryManagementGUI(root)

# Start the GUI loop
root.mainloop()
