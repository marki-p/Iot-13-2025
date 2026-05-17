import tkinter as tk
from task import calculate_max_wire_length
import math
import random

def get_optimal_path(w, heights):
    n = len(heights)
    if n < 2: return [heights[0]] if n == 1 else []
    dp = [[0.0, 0.0] for _ in range(n)]
    parent = [[0, 0] for _ in range(n)]
    for i in range(1, n):
        d00 = dp[i-1][0] + (w**2 + (1-1)**2)**0.5
        d10 = dp[i-1][1] + (w**2 + (heights[i-1]-1)**2)**0.5
        if d00 >= d10: dp[i][0] = d00; parent[i][0] = 0
        else: dp[i][0] = d10; parent[i][0] = 1
        d01 = dp[i-1][0] + (w**2 + (1-heights[i])**2)**0.5
        d11 = dp[i-1][1] + (w**2 + (heights[i-1]-heights[i])**2)**0.5
        if d01 >= d11: dp[i][1] = d01; parent[i][1] = 0
        else: dp[i][1] = d11; parent[i][1] = 1
    curr = 0 if dp[n-1][0] > dp[n-1][1] else 1
    path = []
    for i in range(n-1, -1, -1):
        path.append(1 if curr == 0 else heights[i])
        if i > 0: curr = parent[i][curr]
    path.reverse()
    return path

class ElectricVisualizer:
    def __init__(self, w_val, heights):
        self.w_val = w_val; self.heights = heights; self.n = len(heights)
        self.best_heights = get_optimal_path(w_val, heights)
        self.total_len = calculate_max_wire_length(w_val, heights)
        
        self.STEP_X = 120
        self.SCALE_Y = 5
        self.max_h_limit = max(heights)
        
        self.WIN_W = 1100
        self.WIN_H = 750
        
        content_w = (self.n - 1) * self.STEP_X
        content_h = self.max_h_limit * self.SCALE_Y
        
        self.PAD_X = max(100, (self.WIN_W - content_w) // 2)
        self.PAD_Y = max(150, (self.WIN_H - content_h - 100) // 2)
        
        self.scroll_w = content_w + 2 * self.PAD_X
        self.scroll_h = max(650, content_h + 2 * self.PAD_Y)

        self.root = tk.Tk()
        self.root.title("Візуалізація")
        self.root.geometry(f"{self.WIN_W}x{self.WIN_H}")
        
        self.beers = [] 
        self.pole_states = [0.0 for _ in range(self.n)] 
        self.pole_broken = [False for _ in range(self.n)]
        self.wire_sag = [0.0 for _ in range(self.n - 1)]
        self.shake_amount = 0
        
        self.setup_ui()
        self.draw_everything()
        self.animate()
        
    def setup_ui(self):
        self.header_frame = tk.Frame(self.root, pady=15, bg="#f8f8f8")
        self.header_frame.pack(fill="x")
        
        summary_text = f"Довжина між стовпами: {self.w_val};  К-сть Стовпів: {self.n};  Максимальна довжина дроту: {self.total_len:.2f}"
        tk.Label(self.header_frame, text=summary_text, font=("Arial", 12, "bold"), bg="#f8f8f8").pack(side="left", padx=20)
        
        tk.Button(self.header_frame, text=" ❌ ", command=self.reset_all, 
                 font=("Arial", 11, "bold"), bg="#ff6666", fg="white", relief="raised").pack(side="right", padx=15)

        tk.Button(self.header_frame, text="🍺 ПИВО", command=self.spawn_mass_beer, 
                 font=("Arial", 11, "bold"), bg="gold", fg="black", relief="raised").pack(side="right", padx=15)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.main_frame, bg="white", scrollregion=(0, 0, self.scroll_w, self.scroll_h))
        hbar = tk.Scrollbar(self.main_frame, orient="horizontal", command=self.canvas.xview)
        hbar.pack(side="bottom", fill="x")
        vbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        vbar.pack(side="right", fill="y")
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

    def spawn_mass_beer(self):
        x_start, x_end = self.canvas.xview()
        v_min, v_max = x_start * self.scroll_w, x_end * self.scroll_w
        y_start, _ = self.canvas.yview()
        y_v_min = y_start * self.scroll_h
        
        for _ in range(random.randint(10, 15)):
            x = random.uniform(v_min + 30, v_max - 30)
            y = y_v_min - random.uniform(100, 300)
            bid = self.canvas.create_text(x, y, text="🍺", font=("Arial", 70))
            self.beers.append({
                'id': bid, 'x': x, 'y': y, 'vx': random.uniform(-6, 6), 'vy': 12, 
                'angle': random.uniform(0, 360), 'rot_speed': random.uniform(-15, 15),
                'state': 'flying', 'last_hit_pole': -1, 'last_hit_wire': -1
            })

    def reset_all(self):
        for b in self.beers: self.canvas.delete(b['id'])
        self.beers = []; self.pole_states = [0.0 for _ in range(self.n)]
        self.pole_broken = [False for _ in range(self.n)]; self.wire_sag = [0.0 for _ in range(self.n - 1)]
        self.shake_amount = 0; self.draw_everything()

    def animate(self):
        ground_y = self.scroll_h - self.PAD_Y
        if self.shake_amount > 0:
            dx = random.randint(-self.shake_amount, self.shake_amount)
            dy = random.randint(-self.shake_amount, self.shake_amount)
            self.canvas.move("all", dx, dy); self.shake_amount -= 2

        for b in self.beers:
            if b['state'] == 'flying':
                b['vy'] += 0.5; b['x'] += b['vx']; b['y'] += b['vy']; b['angle'] += b['rot_speed']
                
                # Pole Collision
                for i in range(self.n):
                    if i == b['last_hit_pole']: continue
                    tx, ty = self.to_screen(i, self.best_heights[i], self.pole_states[i])
                    if ((b['x']-tx)**2 + (b['y']-ty)**2)**0.5 < 55:
                        self.pole_broken[i] = True; self.shake_amount = 12
                        b['vy'] = -abs(b['vy']) * 0.9 - random.uniform(15, 25)
                        b['vx'] = (b['x']-tx)*0.6 + random.uniform(-12, 12); b['rot_speed'] = random.uniform(-40, 40)
                        b['last_hit_pole'] = i; b['last_hit_wire'] = -1; break
                
                # Wire Collision
                if b['vy'] > 0 and b['state'] == 'flying':
                    for i in range(self.n - 1):
                        if i == b['last_hit_wire']: continue
                        x1, y1 = self.to_screen(i, self.best_heights[i], self.pole_states[i])
                        x2, y2 = self.to_screen(i+1, self.best_heights[i+1], self.pole_states[i+1])
                        if min(x1, x2)-30 <= b['x'] <= max(x1, x2)+30:
                            t = (b['x']-x1)/(x2-x1+0.001)
                            if 0 <= t <= 1:
                                wire_y = (1-t)*y1 + t*y2 + self.wire_sag[i]*4*t*(1-t)
                                if abs(b['y']-wire_y) < 40:
                                    if abs(b['vy']) < 18: 
                                        b['state'] = 'on_wire'; b['wire_idx'] = i; b['vx']=0; b['vy']=0; b['rot_speed']=0
                                    else:
                                        b['vy'] = -b['vy']*0.5; b['last_hit_wire'] = i; self.wire_sag[i]+=12; break
                
                if b['y'] >= ground_y:
                    if abs(b['vy']) > 5: b['y']=ground_y-5; b['vy']=-b['vy']*0.4; b['vx']*=0.7
                    else: b['y']=ground_y; b['state']='ground'; b['vx']=0; b['vy']=0; b['rot_speed']=0; b['angle']=random.uniform(-10, 10)
                if b['x'] < 0 or b['x'] > self.scroll_w: b['vx']=-b['vx']*0.8; b['x']=max(0, min(self.scroll_w, b['x']))
                self.canvas.coords(b['id'], b['x'], b['y']); self.canvas.itemconfig(b['id'], angle=b['angle'])

            elif b['state'] == 'on_wire':
                idx = b['wire_idx']; self.wire_sag[idx] += 1.8
                if self.wire_sag[idx] > 35: self.pole_broken[idx]=True; self.pole_broken[idx+1]=True
                x1, y1 = self.to_screen(idx, self.best_heights[idx], self.pole_states[idx])
                x2, y2 = self.to_screen(idx+1, self.best_heights[idx+1], self.pole_states[idx+1])
                t = (b['x']-x1)/(x2-x1+0.001); b['y'] = (1-t)*y1 + t*y2 + self.wire_sag[idx]*4*t*(1-t)
                self.canvas.coords(b['id'], b['x'], b['y'])
                if b['y'] >= ground_y: b['state']='ground'; b['y']=ground_y

        for i in range(self.n):
            if self.pole_broken[i] and self.pole_states[i] < 1.0: self.pole_states[i] = min(1.0, self.pole_states[i] + 0.08)
        for i in range(self.n - 1):
            if self.pole_broken[i] or self.pole_broken[i+1]:
                self.wire_sag[i] = max(self.wire_sag[i], 50 * max(self.pole_states[i], self.pole_states[i+1]))

        self.draw_everything()
        self.root.after(25, self.animate)

    def to_screen(self, i, h, angle_factor=0.0):
        bx = self.PAD_X + i * self.STEP_X; by = self.scroll_h - self.PAD_Y; length = h * self.SCALE_Y
        angle = angle_factor * (math.pi / 2.01)
        return bx + length * math.sin(angle), by - length * math.cos(angle)

    def draw_everything(self):
        self.canvas.delete("pole_obj")
        ground_y = self.scroll_h - self.PAD_Y
        self.canvas.create_line(self.PAD_X-200, ground_y, self.scroll_w+200, ground_y, fill="#222222", width=5, tags="pole_obj")

        pole_pts = []
        for i in range(self.n):
            h = self.best_heights[i]; bx, by = self.PAD_X + i * self.STEP_X, ground_y
            tx, ty = self.to_screen(i, h, self.pole_states[i]); pole_pts.append((tx, ty))
            # Draw Pole
            self.canvas.create_line(bx, by, tx, ty, width=8, fill="black", tags="pole_obj")
            # Restored Pole Height Label
            if self.pole_states[i] < 0.2:
                self.canvas.create_text(bx - 30, (by + ty)/2, text=str(h), angle=90, fill="#777777", font=("Arial", 10), tags="pole_obj")
            self.canvas.create_oval(tx-6, ty-6, tx+6, ty+6, fill="red", outline="black", tags="pole_obj")
            self.canvas.create_text(bx, by + 35, text=f"т{i+1}", font=("Arial", 12, "bold"), tags="pole_obj")

        for i in range(self.n - 1):
            x1, y1 = pole_pts[i]; x2, y2 = pole_pts[i+1]; sag = self.wire_sag[i]
            if sag <= 0:
                self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=3, tags="pole_obj")
                # Restored Wire Length Label
                dx, dy = x2 - x1, y2 - y1; dist = (self.w_val**2 + (self.best_heights[i+1]-self.best_heights[i])**2)**0.5
                angle_deg = -math.degrees(math.atan2(dy, dx))
                mx, my = (x1+x2)/2, (y1+y2)/2
                nx, ny = -dy/((dx**2+dy**2)**0.5+0.1), dx/((dx**2+dy**2)**0.5+0.1)
                if ny > 0: nx, ny = -nx, -ny
                self.canvas.create_text(mx + nx*25, my + ny*25, text=f"{dist:.2f}", angle=angle_deg, fill="blue", font=("Arial", 10, "bold"), tags="pole_obj")
            else:
                mx = (x1 + x2) / 2; my = (y1 + y2) / 2 + sag * 2.0
                self.canvas.create_line(x1, y1, mx, my, x2, y2, fill="blue", width=3, smooth=True, tags="pole_obj")

    def run(self): self.root.mainloop()

def visualize():
    try:
        with open('data.in', 'r') as f: data = f.read().split()
        if not data: return
        w_val = int(data[0]); heights = [int(x) for x in data[1:]]
        ElectricVisualizer(w_val, heights).run()
    except: return

if __name__ == "__main__": visualize()
