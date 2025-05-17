# Multi-Threaded File Downloader (Interactive)

This project is a Python-based multi-threaded downloader that allows users to download multiple files (TXT, PDF, CSV, etc.) from URLs using threading and progress bars. It supports automatic folder creation and retry logic, and logs all download events.

---

## Features

- ✅ Interactive input (no CLI needed)
- ✅ Download multiple files concurrently
- ✅ Supports any file type (user-defined)
- ✅ Download retry mechanism
- ✅ Progress bars using `tqdm`
- ✅ Logs errors and statuses to `download_log.txt`

---

## 🖥️ Requirements

Make sure you have Python 3.7+ installed.

Install required libraries:

```bash
pip install requests tqdm
```
## How to Run
```bash
python downloader.py
```
## Output Folder
```
downloads/
└── [file_type]/
    ├── file1.txt
    ├── file2.txt
```
