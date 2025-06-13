
import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import sqlite3
import os
import smtplib
from email.message import EmailMessage

DB_NAME = "hash_database.db"

# Define allowed extensions
ALLOWED_EXTENSIONS = {".bat", ".conf", ".csv", ".dll", ".doc", ".docx", ".ini", ".jpeg", ".jpg",
                      ".json", ".log", ".pdf", ".png", ".ppt", ".pptx", ".py", ".sh", ".txt", 
                      ".xls", ".xlsx", ".xml", ".yaml", ".yml"}

# Email Configuration
EMAIL_SENDER = "youremail@gmail.com"
EMAIL_PASSWORD = "yourapppassword"
EMAIL_RECEIVER = "receiveremail@gmail.com"

def send_email_notification(file_path):
    msg = EmailMessage()
    msg.set_content(f"Alert: File has been modified: {file_path}")
    msg["Subject"] = "File Integrity Alert"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

# --- DB Setup ---
def create_table():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS file_hashes (filepath TEXT PRIMARY KEY, hash TEXT NOT NULL)")
        conn.commit()

# --- Hash Function ---
def calculate_hash(file_path):
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file:\n{e}")
        return None

# --- Add File ---
def add_to_database():
    if not selected_file.get():
        return
    ext = os.path.splitext(selected_file.get())[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        messagebox.showerror("Invalid File", f"Extension '{ext}' is not monitored.")
        return
    hash_val = calculate_hash(selected_file.get())
    if hash_val:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT OR REPLACE INTO file_hashes (filepath, hash) VALUES (?, ?)", (selected_file.get(), hash_val))
                conn.commit()
                messagebox.showinfo("Success", "File added to database.")
            except Exception as e:
                messagebox.showerror("DB Error", str(e))

# --- Check File ---
def check_file():
    if not selected_file.get():
        return
    hash_val = calculate_hash(selected_file.get())
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT hash FROM file_hashes WHERE filepath=?", (selected_file.get(),))
        row = c.fetchone()
        if row:
            if row[0] == hash_val:
                messagebox.showinfo("Integrity Check", "File is unmodified ✅")
            else:
                messagebox.showwarning("Integrity Check", "File has been modified ⚠️")
                send_email_notification(selected_file.get())
        else:
            messagebox.showwarning("Not Found", "File not found in database.")

# --- File Picker ---
def choose_file():
    file_path = filedialog.askopenfilename()
    selected_file.set(file_path)

# --- GUI Setup ---
create_table()
root = tk.Tk()
root.title("FIMbyDOXX1011")

selected_file = tk.StringVar()

tk.Label(root, text="Selected file:").pack(pady=5)
tk.Entry(root, textvariable=selected_file, width=50).pack(pady=5)
tk.Button(root, text="Browse", command=choose_file).pack(pady=5)
tk.Button(root, text="Add to Database", command=add_to_database).pack(pady=5)
tk.Button(root, text="Check Integrity", command=check_file).pack(pady=5)

root.mainloop()
