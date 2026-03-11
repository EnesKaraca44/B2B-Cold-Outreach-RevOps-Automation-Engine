# 🚀 B2B Cold Outreach & RevOps Automation Engine

![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge) 
![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge)
![Tech](https://img.shields.io/badge/Python-3.10-yellow?style=for-the-badge&logo=python) 
![UI](https://img.shields.io/badge/Streamlit-UI-red?style=for-the-badge&logo=streamlit) 
![AI](https://img.shields.io/badge/AI-Gemini_LLM-purple?style=for-the-badge)

A powerful, fully-automated **Sales Development Representative (SDR) & Revenue Operations (RevOps)** tool built with Python. This system automates the entire top-of-funnel B2B sales process: from prospect discovery via intelligent web scraping, to hyper-personalized AI icebreaker generation, and finally, automated cold email outreach sequences.

## 🎯 Architecture & Features

This tool replaces expensive SaaS subscriptions (like Apollo.io, Lemlist, or ZoomInfo) with a custom, scalable Python architecture.

*   **🔍 Intelligent Prospecting (Dorking Engine):** Seamlessly integrates with the DuckDuckGo Search API to bypass common Google HTTP 429 blocks. Simply input a niche (e.g., "Software Agencies in London") and the engine automatically finds highly relevant business domains.
*   **🕷️ Robust Web Scraper:** Crawls target websites and their sub-directories (like `/contact` pages) using `BeautifulSoup` and sophisticated regex patterns to extract direct B2B email addresses.
*   **🧠 Hyper-Personalized GenAI (Google Gemini):** Connects to the LLM via API to analyze the scraped target. It dynamically generates context-aware, highly personalized "Icebreaker" sentences for each prospect, dramatically increasing cold email open and reply rates.
*   **✉️ SMTP Delivery Engine:** Features a built-in bulk email sender using Python's `smtplib`. It sends out the HTML-formatted, AI-injected cold emails automatically, complete with anti-spam sleep intervals between sends.
*   **📊 Streamlit SaaS Interface:** A clean, wizard-style user interface built with Streamlit. It includes a live dashboard for tracking metrics (Total Scraped, Valid Emails Found, AI Generation Status) and features single-click CSV export options.

## ⚙️ Tech Stack

*   **Core:** Python 3.10+
*   **UI Framework:** Streamlit (`app.py`)
*   **Web Scraping:** `BeautifulSoup4`, `requests`
*   **Search Engine Integration:** `duckduckgo-search`
*   **AI / LLM:** Google generative AI API (Gemini-1.5-flash)
*   **Data Processing:** `pandas`
*   **Emailing:** Built-in `smtplib` & `email.mime`

## 🚀 Getting Started

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/b2b-revops-engine.git
    cd b2b-revops-engine
    ```
2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure API Keys**
    *   Open `ai_generator.py` and replace the placeholder `GEMINI_API_KEY` with your free Google AI Studio key.
    *   (Optional for Emailing) Open `app.py` UI and use your Gmail App Password.
4.  **Run the Interface**
    ```bash
    streamlit run app.py
    ```

## 🤝 For Clients (SalesOps Consulting)

If you are a B2B company looking to implement this system into your own CRM (HubSpot, Salesforce) or want a custom RevOps pipeline built from scratch, **I offer freelance Sales Engineering & Automation consulting**. 

Capabilities include:
*   Integrating scraped data directly via Webhooks/Zapier.
*   Building multi-step email drip campaigns.
*   Bypassing tough scraper captchas for specific enterprise targets.

📫 **Contact me on LinkedIn or Upwork to discuss your Revenue Operations.**

---
*Built with logic and efficiency by Enes Karaca (KDS Software Team)*
