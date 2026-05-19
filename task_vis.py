import tkinter as tk
from tkinter import messagebox
import time
import math
import winsound

import os

def play_match_sound():
    # Soft and satisfying 'double-pluck' chime
    paths = [
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Media', 'Windows Information Bar.wav'),
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Media', 'Speech On.wav'),
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Media', 'Windows Navigation Start.wav')
    ]
    for p in paths:
        if os.path.exists(p):
            winsound.PlaySound(p, winsound.SND_FILENAME | winsound.SND_ASYNC)
            return
    winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)

def play_step_sound():
    # Primary sound: Information Bar
    # Secondary: Navigation Start
    paths = [
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Media', 'Windows Navigation Start.wav'),
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Media', 'Speech On.wav')
    ]
    for p in paths:
        if os.path.exists(p):
            winsound.PlaySound(p, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
            return
    # Fallback to a standard system sound that exists on all Windows
    winsound.PlaySound("SystemDefault", winsound.SND_ALIAS | winsound.SND_ASYNC)

def play_grand_final_sound():
    # Beautiful ascending musical chime
    paths = [
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Media', 'Windows Unlock.wav'),
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Media', 'Windows Feed Discovered.wav'),
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Media', 'tada.wav')
    ]
    for p in paths:
        if os.path.exists(p):
            winsound.PlaySound(p, winsound.SND_FILENAME | winsound.SND_ASYNC)
            return
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)

def compute_prefix_function(p):
    m = len(p)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k > 0 and p[k] != p[q]:
            k = pi[k-1]
        if p[k] == p[q]:
            k += 1
        pi[q] = k
    return pi

class KMPVisualizer:
    def __init__(self, root, needle, haystack):
        self.root = root
        self.root.title("Метод Кнутта-Морріса-Прата")
        self.needle = needle
        self.haystack = haystack
        self.pi = compute_prefix_function(needle)
        
        self.n = len(haystack)
        self.m = len(needle)
        
        self.cell_size = 40
        self.start_x = 160
        self.total_width = self.start_x + (self.n + 2) * self.cell_size
        
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.main_frame, width=min(1200, self.total_width), height=400, bg="#f0f0f0")
        self.hbar = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.hbar.set)
        
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.canvas.configure(scrollregion=(0, 0, self.total_width, 400))
        
        self.controls = tk.Frame(root, bg="#f0f0f0")
        self.controls.pack(pady=10)
        
        self.start_btn = tk.Button(self.controls, text="Старт", command=self.run_visualization, 
                                   bg="#4caf50", fg="white", font=("Arial", 10, "bold"), padx=20)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.speed = 0.4
        self.haystack_y = 120
        self.needle_y = 170
        self.pi_y = 300
        
        self.current_needle_offset = 0.0
        self.match_indices = []
        self.current_status_text = "Натисніть 'Старт', щоб почати"

    def draw_array(self, arr, y, label, highlight_idx=-1, color="lightblue"):
        self.canvas.create_text(self.start_x - 10, y + self.cell_size/2, text=label, anchor="e", font=("Arial", 10, "bold"))
        for i, char in enumerate(arr):
            x1 = self.start_x + i * self.cell_size
            y1 = y
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            fill = color if i == highlight_idx else "white"
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#ccc", width=1)
            self.canvas.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, text=str(char), font=("Arial", 10))

    def update_display(self, haystack_idx=-1, active_needle_idx=-1):
        self.canvas.delete("all")
        
        # Center of the current visible part of the canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1: canvas_width = 1200
        if canvas_height <= 1: canvas_height = 400
        
        mid_y = canvas_height / 2
        self.haystack_y = mid_y - 80
        self.needle_y = mid_y - 30
        self.pi_y = mid_y + 80
        
        left_x = self.canvas.xview()[0] * self.total_width
        center_visible_x = left_x + canvas_width / 2

        # 0. Draw Algorithm Title at a FIXED position on the canvas
        self.canvas.create_text(20, 25, 
                                text="Метод Кнутта-Морріса-Прата", 
                                font=("Arial", 18, "bold"), fill="#1a237e", anchor="nw")

        # 1. Draw Grid/Arrays
        self.draw_array(self.haystack, self.haystack_y, "Текст (Haystack):", haystack_idx, "#fff176")
        self.draw_array(self.pi, self.pi_y, "Таблиця Pi:")
        
        # 2. Highlight matches and draw "Кількість входжень: X" text above the LATEST one
        for j, idx in enumerate(self.match_indices):
            x1 = self.start_x + idx * self.cell_size
            
            # Green rectangle for all matches
            self.canvas.create_rectangle(x1, self.haystack_y, x1 + self.cell_size * self.m, self.haystack_y + self.cell_size, 
                                         outline="#4caf50", width=3)
            
            # Text ONLY above the most recent match
            if j == len(self.match_indices) - 1:
                x_mid = x1 + (self.m * self.cell_size) / 2
                self.canvas.create_text(x_mid, self.haystack_y - 25, 
                                         text=f"Кількість входжень: {j+1}", 
                                         font=("Arial", 11, "bold"), fill="#2e7d32")

        # 3. Draw Needle
        self.draw_needle(active_needle_idx)
        
        # 4. Draw status text following the needle (dynamic position)
        if haystack_idx != -1:
            status_x = self.start_x + (self.current_needle_offset + self.m/2) * self.cell_size
            status_y = self.needle_y + self.cell_size + 30
            self.canvas.create_text(status_x, status_y, text=self.current_status_text, 
                                     font=("Arial", 11, "bold"), fill="#333", anchor="n")
        
        self.auto_scroll(haystack_idx)

    def draw_needle(self, active_idx):
        y = self.needle_y
        for i, char in enumerate(self.needle):
            x1 = self.start_x + (self.current_needle_offset + i) * self.cell_size
            y1 = y
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            fill = "#ffb74d" if i == active_idx else "white"
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#ccc")
            self.canvas.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, text=str(char))

    def smooth_scroll(self, target_view_pos):
        current_pos = self.canvas.xview()[0]
        steps = 5
        for i in range(steps + 1):
            t = i / steps
            ease = t*t * (3 - 2*t)
            pos = current_pos + (target_view_pos - current_pos) * ease
            self.canvas.xview_moveto(pos)
            self.root.update()
            time.sleep(0.005)

    def auto_scroll(self, idx):
        if idx == -1: return
        self.root.update_idletasks()
        curr_x = self.start_x + idx * self.cell_size
        canvas_width = self.canvas.winfo_width()
        
        target_view_start = (curr_x + self.cell_size / 2 - canvas_width / 2) / self.total_width
        target_view_start = max(0, min(1, target_view_start))
        
        self.smooth_scroll(target_view_start)

    def animate_needle_move(self, target_offset, active_idx):
        start_offset = self.current_needle_offset
        steps = 5
        for i in range(steps + 1):
            t = i / steps
            ease = t*t * (3 - 2*t)
            self.current_needle_offset = start_offset + (target_offset - start_offset) * ease
            self.update_display(active_needle_idx=active_idx)
            self.root.update()
            time.sleep(0.005)

    def run_visualization(self):
        play_step_sound() # <--- ЦЕЙ ЗВУК ТЕПЕР ТУТ ПЕРШИМ
        self.start_btn.config(state=tk.DISABLED, bg="#ccc")
        self.match_indices = []
        self.current_needle_offset = 0.0
        q = 0
        
        for i in range(self.n):
            target_offset = i - q
            if abs(self.current_needle_offset - target_offset) > 0.1:
                self.animate_needle_move(target_offset, q)
            
            play_step_sound() # Sound for each step
            self.current_status_text = f"Порівнюємо: '{self.haystack[i]}' та '{self.needle[q]}'"
            self.update_display(i, q)
            self.root.update()
            time.sleep(self.speed)
            
            while q > 0 and self.needle[q] != self.haystack[i]:
                old_q = q
                q = self.pi[q-1]
                self.current_status_text = f"Незбіг! Зсуваємо за допомогою Pi: {old_q} -> {q}"
                self.animate_needle_move(i - q, q)
                time.sleep(self.speed)
                
            if self.needle[q] == self.haystack[i]:
                q += 1
                self.current_status_text = f"Збіг! q={q}"
            else:
                self.current_status_text = "Незбіг, рухаємося далі."
                
            if q == self.m:
                match_start = i - self.m + 1
                self.match_indices.append(match_start)
                play_match_sound() # Play sound for match
                self.current_status_text = f"Входження знайдено на індексі {match_start}!"
                self.update_display(i, q-1)
                time.sleep(self.speed * 1.5)
                q = self.pi[q-1]
                self.animate_needle_move(i - q + 1, q)

        self.current_status_text = f"Готово! Знайдено на індексах: {self.match_indices}"
        self.update_display(-1, -1)
        play_grand_final_sound() # Final grand sound
        self.start_btn.config(state=tk.NORMAL, bg="#4caf50")

def main():
    try:
        with open('data.in', 'r', encoding='utf-8') as f:
            lines = [line.strip('\n\r') for line in f.readlines() if line.strip('\n\r')]
            if len(lines) < 2: return
            haystack = lines[0]
            needle = lines[1]
    except FileNotFoundError: return

    root = tk.Tk()
    root.configure(bg="#f0f0f0")
    
    # Set 16:9 aspect ratio (e.g., 1024x576 or 1280x720)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    width = int(screen_width * 0.7)
    height = int(width * 9 / 16)
    
    # Ensure it doesn't exceed screen height
    if height > screen_height * 0.8:
        height = int(screen_height * 0.8)
        width = int(height * 16 / 9)
        
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    app = KMPVisualizer(root, needle, haystack)
    root.mainloop()

if __name__ == "__main__":
    main()
