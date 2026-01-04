import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from database.repository import (
    get_stats_top_mechanics, 
    get_stats_top_parts, 
    get_stats_deviz_status, 
    get_stats_revenue_trend
)

class StatisticsDashboard:
    def __init__(self, parent, db_conn):
        self.db_conn = db_conn
        self.win = ttk.Toplevel(parent)
        self.win.title("Statistici Avansate & Performanță")
        self.win.geometry("1300x850")
        
        # Container Principal
        main = ttk.Frame(self.win, padding=20)
        main.pack(fill=BOTH, expand=True)
        
        # Header
        h_frame = ttk.Frame(main)
        h_frame.pack(fill=X, pady=(0,20))
        ttk.Label(h_frame, text="📈 Dashboard Managerial", font=("Segoe UI", 24, "bold"), bootstyle="primary").pack(side=LEFT)
        ttk.Button(h_frame, text="ÎNCHIDE", command=self.win.destroy, bootstyle="secondary-outline").pack(side=RIGHT)

        # Grid pentru Grafice (2x2)
        grid = ttk.Frame(main)
        grid.pack(fill=BOTH, expand=True)
        grid.columnconfigure(0, weight=1); grid.columnconfigure(1, weight=1)
        grid.rowconfigure(0, weight=1); grid.rowconfigure(1, weight=1)
        
        self.create_chart_1(grid) # Top Mecanici
        self.create_chart_2(grid) # Top Piese
        self.create_chart_3(grid) # Status Devize
        self.create_chart_4(grid) # Trend Venituri

    def _setup_fig(self, title):
        """ Helper pentru stilizarea graficelor pe fundal dark """
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor('#2b3e50') # Culoare fundal Superhero
        ax = fig.add_subplot(111)
        ax.set_facecolor('#2b3e50')
        ax.set_title(title, color='white', fontsize=12, pad=20)
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        for spine in ax.spines.values(): spine.set_color('white')
        return fig, ax

    def _embed(self, fig, parent, r, c):
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        w = canvas.get_tk_widget()
        w.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")

    def create_chart_1(self, parent):
        # Top Mecanici (Bar Chart Orizontal)
        data = get_stats_top_mechanics(self.db_conn)
        fig, ax = self._setup_fig("🏆 Top Mecanici (Ore Lucrate)")
        
        if data:
            names = [x[0] for x in data][::-1]
            hours = [float(x[1]) for x in data][::-1]
            bars = ax.barh(names, hours, color='#5bc0de') # Info blue
            ax.bar_label(bars, color='white', padding=3)
        else:
            ax.text(0.5, 0.5, "Nu sunt date", color='white', ha='center')
        
        self._embed(fig, parent, 0, 0)

    def create_chart_2(self, parent):
        # Top Piese (Bar Chart Vertical)
        data = get_stats_top_parts(self.db_conn)
        fig, ax = self._setup_fig("📦 Top Piese Vândute")
        
        if data:
            names = [x[0] for x in data]
            qty = [float(x[1]) for x in data]
            bars = ax.bar(names, qty, color='#f0ad4e') # Warning orange
            ax.bar_label(bars, color='white')
            plt.setp(ax.get_xticklabels(), rotation=30, ha="right") # Rotim etichetele
        
        fig.tight_layout()
        self._embed(fig, parent, 0, 1)

    def create_chart_3(self, parent):
        # Status Devize (Donut Chart)
        data = get_stats_deviz_status(self.db_conn)
        fig, ax = self._setup_fig("📋 Status Comenzi Service")
        
        if data:
            labels = [x[0] for x in data]
            counts = [x[1] for x in data]
            colors = ['#d9534f', '#5cb85c', '#5bc0de', '#f0ad4e'] # Culori bootstrap
            wedges, texts, autotexts = ax.pie(counts, labels=labels, autopct='%1.1f%%', 
                                              startangle=90, colors=colors, 
                                              textprops={'color':"white"}, pctdistance=0.85)
            # Facem gaura la mijloc (Donut)
            centre_circle = plt.Circle((0,0),0.70,fc='#2b3e50')
            fig.gca().add_artist(centre_circle)
        
        self._embed(fig, parent, 1, 0)

    def create_chart_4(self, parent):
        # Trend Venituri (Line Chart)
        data = get_stats_revenue_trend(self.db_conn)
        fig, ax = self._setup_fig("💰 Evoluție Venituri (Ultimile 6 luni)")
        
        if data:
            months = [x[0] for x in data][::-1]
            values = [float(x[1]) for x in data][::-1]
            
            ax.plot(months, values, marker='o', linestyle='-', color='#5cb85c', linewidth=2)
            ax.fill_between(months, values, color='#5cb85c', alpha=0.3) # Umbra sub linie
            ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
            
            for i, v in enumerate(values):
                ax.text(i, v + (max(values)*0.05), f"{int(v)}", color='white', ha='center')

        self._embed(fig, parent, 1, 1)

def open_statistics_window(parent, conn):
    StatisticsDashboard(parent, conn)