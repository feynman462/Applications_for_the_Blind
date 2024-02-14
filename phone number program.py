import csv
import tkinter as tk
from tkinter import filedialog

def browse_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        csv_entry.delete(0, tk.END)
        csv_entry.insert(tk.END, file_path)

def search_phone():
    file_path = csv_entry.get()
    search_term = phone_entry.get()
    results.delete(1.0, tk.END)

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for field in row:
                if search_term in field:
                    results.insert(tk.END, ', '.join(row) + '\n')
                    break

def on_entry_click(event):
    if event.widget.get() == event.widget.default_text:
        event.widget.delete(0, "end")
        event.widget.config(fg="black")

def on_entry_focusout(event):
    if not event.widget.get():
        event.widget.insert(0, event.widget.default_text)
        event.widget.config(fg="grey")

root = tk.Tk()
root.title("Phone Number Search")

frame = tk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10)

csv_label = tk.Label(frame, text="CSV File:")
csv_label.grid(row=0, column=0)
csv_entry = tk.Entry(frame, width=40)
csv_entry.default_text = "Click or use tab key to enter the CSV file path"
csv_entry.insert(0, csv_entry.default_text)
csv_entry.bind("<FocusIn>", on_entry_click)
csv_entry.bind("<FocusOut>", on_entry_focusout)
csv_entry.config(fg="grey")
csv_entry.grid(row=0, column=1)
browse_button = tk.Button(frame, text="Browse", command=browse_csv)
browse_button.grid(row=0, column=2)

phone_label = tk.Label(frame, text="Phone Number:")
phone_label.grid(row=1, column=0)
phone_entry = tk.Entry(frame, width=40)
phone_entry.default_text = "Click or use tab key to enter the phone number"
phone_entry.insert(0, phone_entry.default_text)
phone_entry.bind("<FocusIn>", on_entry_click)
phone_entry.bind("<FocusOut>", on_entry_focusout)
phone_entry.config(fg="grey")
phone_entry.grid(row=1, column=1)

search_button = tk.Button(frame, text="Search", command=search_phone)
search_button.grid(row=2, column=1)

results_label = tk.Label(frame, text="Results:")
results_label.grid(row=3, column=0)
results = tk.Text(frame, wrap=tk.WORD, width=60, height=10)
results.grid(row=4, column=0, columnspan=3)

root.mainloop()
python "C:\Users\remz_\Documents\flash card game.py" > "flash card game program_output.txt" 2>&1
