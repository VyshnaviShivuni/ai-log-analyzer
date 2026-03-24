# AI Log Analyzer

## Live Demo

https://loganalyzerai.streamlit.app/

AI-powered tool for analyzing application logs to identify errors, determine root causes, and suggest fixes using large language models.

---

## Overview

This application allows users to upload log files and receive structured insights to reduce manual debugging effort and improve issue resolution time.

---

## Features

- Upload `.txt` or `.log` files  
- AI-based log analysis  
- Multiple analysis modes (Standard, Root Cause Only, Concise)  
- Custom user instructions  
- Downloadable analysis report  

---

## Tech Stack

- Python  
- Streamlit  
- Groq API (LLaMA 3.1)  
- python-dotenv  

---

## Setup

```bash
git clone https://github.com/VyshnaviShivuni/ai-log-analyzer.git
cd ai-log-analyzer
pip install -r requirements.txt
```

Run the application:
```bash

streamlit run app.py
```

---

## Use Case

Designed for engineers and developers to quickly analyze logs, identify issues, and reduce debugging time.

---

## Author

Vyshnavi Shivuni