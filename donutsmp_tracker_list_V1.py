import tkinter as tk
from tkinter import ttk, messagebox
import requests

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

def search_items():
    item = item_entry.get()
    sort = sort_var.get()

    if not item:
        messagebox.showerror("Error", "Please enter an item name.")
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
                for entry in items:
                    item_info = entry.get("item", {})
                    display_name = item_info.get("display_name", "Unknown")
                    price = entry.get("price", 0)
                    seller = entry.get("seller", {}).get("name", "Unknown")
                    time_left = entry.get("time_left", "Unknown")

                    results_text.insert(tk.END, f"Item: {display_name}\n")
                    results_text.insert(tk.END, f"Price: ${price:,}\n")
                    results_text.insert(tk.END, f"Seller: {seller}\n")
                    results_text.insert(tk.END, f"Time Left: {time_left} seconds\n")
                    results_text.insert(tk.END, "-" * 40 + "\n")
        else:
            results_text.insert(tk.END, f"API Error: {response.status_code}\n{response.text}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI Setup
app = tk.Tk()
app.title("DonutSMP Auction Price Tracker")
app.geometry("600x500")

frame = ttk.Frame(app, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="Item Name:").grid(row=0, column=0, sticky="w")
item_entry = ttk.Entry(frame, width=40)
item_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="Sort By:").grid(row=1, column=0, sticky="w")
sort_var = tk.StringVar(value=SORT_OPTIONS[0])
sort_menu = ttk.Combobox(frame, textvariable=sort_var, values=SORT_OPTIONS, state="readonly")
sort_menu.grid(row=1, column=1, padx=5, pady=5)

search_btn = ttk.Button(frame, text="Search", command=search_items)
search_btn.grid(row=2, column=0, columnspan=2, pady=10)

results_text = tk.Text(frame, height=20)
results_text.grid(row=3, column=0, columnspan=2, sticky="nsew")

frame.grid_rowconfigure(3, weight=1)
frame.grid_columnconfigure(1, weight=1)

footer_label = ttk.Label(app, text="Made by Dog_On_New_PC", anchor="e", font=("Arial", 8))
footer_label.place(relx=1.0, rely=1.0, anchor="se", x=-250, y=-10)
app.mainloop()
