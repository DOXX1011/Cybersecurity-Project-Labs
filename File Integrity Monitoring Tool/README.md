# 🛡️ FIMbyDOXX1011 – File Integrity Monitoring Tool

[![Python](https://img.shields.io/badge/python-3.10+-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)]()
[![GUI](https://img.shields.io/badge/interface-Tkinter-blue)]()

**FIMbyDOXX1011** is a lightweight and customizable File Integrity Monitoring (FIM) tool designed for cybersecurity students, blue teamers, and system administrators. It helps you keep track of sensitive files in real-time and alerts you via email if any unauthorized modifications are detected.

---

## ✨ Features

- ✅ Real-time **directory monitoring**
- 🎯 Focus on **critical file extensions**:
  `.bat`, `.conf`, `.csv`, `.dll`, `.doc`, `.docx`, `.ini`, `.jpeg`, `.jpg`, `.json`, `.log`, `.pdf`, `.png`, `.ppt`, `.pptx`, `.py`, `.sh`, `.txt`, `.xls`, `.xlsx`, `.xml`, `.yaml`, `.yml`
- 🧠 Stores file hashes in **SQLite database**
- 📬 **Gmail alerts** on file change
- 🖥️ **User-friendly GUI** for interaction

---

## 📂 Installation

```bash
git clone https://github.com/yourusername/FIMbyDOXX1011.git
cd FIMbyDOXX1011
pip install -r requirements.txt
python fim_gui.py
