import tkinter as tk
from tkinter import ttk, messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from datetime import datetime
API_KEY = "8256a2471db54a5992b47c46a57f30d3"
API_URL = "https://api.donutsmp.net/v1/auction/list/1"
HEADERS = {
    "accept": "application/json",
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

SORT_OPTIONS = [
    "lowest_price",
    "highest_price",
    "recently_listed",
    "last_listed"
]

refresh_interval = 10  # seconds
price_history = []
time_history = []

def search_items():
    item = item_entry.get()
    sort = sort_var.get()

    if not item:
        return

    data = {
        "search": item,
        "sort": sort
    }

    try:
        response = requests.get(API_URL, headers=HEADERS, json=data)
        results_text.delete("1.0", tk.END)

        if response.status_code == 200:
            json_data = response.json()
            items = json_data.get("result", [])

            if not items:
                results_text.insert(tk.END, "No results found.\n")
            else:
                prices = []
                for entry in items:
                    item_info = entry.get("item", {})
                    display_name = item_info.get("display_name", "Unknown")
                    price = entry.get("price", 0)
                    prices.append(price)

                    seller = entry.get("seller", {}).get("name", "Unknown")
                    time_left = entry.get("time_left", "Unknown")

                    results_text.insert(tk.END, f"Item: {display_name}\n")
                    results_text.insert(tk.END, f"Price: ${price:,}\n")
                    results_text.insert(tk.END, f"Seller: {seller}\n")
                    results_text.insert(tk.END, f"Time Left: {time_left} seconds\n")
                    results_text.insert(tk.END, "-" * 40 + "\n")

                if prices:
                    lowest = min(prices)
                    price_history.append(lowest)
                    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    time_history.append(timestamp)
                    update_graph()
        else:
            results_text.insert(tk.END, f"API Error: {response.status_code}\n{response.text}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
def auto_refresh():
    search_items()
    app.after(refresh_interval * 1000, auto_refresh)
def update_graph():
    ax.clear()
    ax.plot(time_history, price_history, marker='o', color='blue')
    ax.set_title("Price Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Lowest Price")
    ax.tick_params(axis='x', rotation=45)
    graph_canvas.draw()
app = tk.Tk()
app.title("DonutSMP Price Tracker")
app.geometry("1200x700")
main_frame = ttk.Frame(app)
main_frame.pack(fill=tk.BOTH, expand=True)
left_panel = ttk.Frame(main_frame, padding=10)
left_panel.pack(side=tk.LEFT, fill=tk.Y)
ttk.Label(left_panel, text="Item Name:").pack(anchor="w")
item_entry = ttk.Entry(left_panel, width=30)
item_entry.pack(pady=5)
ttk.Label(left_panel, text="Sort By:").pack(anchor="w")
sort_var = tk.StringVar(value=SORT_OPTIONS[0])
sort_menu = ttk.Combobox(left_panel, textvariable=sort_var, values=SORT_OPTIONS, state="readonly", width=28)
sort_menu.pack(pady=5)
search_btn = ttk.Button(left_panel, text="Search", command=search_items)
search_btn.pack(pady=10)
ttk.Label(left_panel, text="Auction Results:").pack(anchor="w", pady=(10, 0))
results_text = tk.Text(left_panel, width=40, height=30)
results_text.pack(fill=tk.Y, expand=True)
right_panel = ttk.Frame(main_frame, padding=10)
right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
fig, ax = plt.subplots(figsize=(10, 5))
graph_canvas = FigureCanvasTkAgg(fig, master=right_panel)
graph_widget = graph_canvas.get_tk_widget()
graph_widget.pack(fill=tk.BOTH, expand=True)
toolbar = NavigationToolbar2Tk(graph_canvas, right_panel)
toolbar.update()
toolbar.pack()
app.after(1000, auto_refresh)
footer_label = ttk.Label(app, text="Made by Dog_On_New_PC        Auto refresh is 10s", anchor="e", font=("Arial", 8))
footer_label.place(relx=1.0, rely=1.0, anchor="se", x=-250, y=-10)
app.mainloop()
