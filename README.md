# DNS Insight – DNS Lookup and Analysis Tool

## 1. Project Overview
DNS Insight is a web-based Domain Name System (DNS) lookup and analysis tool developed as a Data Communication and Networking (DCN) project. It allows users to look up DNS records for a domain and understand basic DNS resolution behavior through a simple dashboard.

## 2. Objectives
- Resolve domain names and retrieve DNS records.
- Display DNS lookup results in a user-friendly interface.
- Measure and display DNS query response time.
- Demonstrate DNS caching and cache statistics.
- Provide a conceptual visualization of the DNS resolution process.
- Maintain a history of previous DNS lookups.

## 3. Features
- DNS lookup for supported record types.
- DNS response time measurement.
- DNS cache management and cache statistics.
- DNS resolution trace visualization.
- Lookup history.
- Basic DNS diagnostic information.
- Interactive dashboard with charts.

## 4. Technologies Used
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python and Flask
- **DNS Library:** dnspython
- **Data Storage:** SQLite
- **Development Tool:** Visual Studio Code
- **Version Control:** Git and GitHub

## 5. Project Structure

```text
dns-insight/
├── backend/
│   ├── app.py
│   ├── cache_manager.py
│   ├── diagnostics.py
│   ├── dns_service.py
│   ├── history_manager.py
│   ├── trace_service.py
│   └── requirements.txt
├── data/
│   └── dns_history.db
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── .gitignore
└── README.md
```

## 6. Installation and Execution

### Step 1: Clone the Repository
```bash
git clone https://github.com/sushmi12307/dns-insight.git
cd dns-insight
```

### Step 2: Create and Activate a Virtual Environment
On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```bash
python -m pip install -r backend/requirements.txt
```

If dependencies are not listed in the requirements file, install them using:

```bash
python -m pip install Flask dnspython
```

### Step 4: Run the Application
```bash
python backend/app.py
```

### Step 5: Open the Application
Open the following address in your browser:

http://127.0.0.1:5000

## 7. How It Works
1. The user enters a domain name and selects a DNS record type.
2. The frontend sends the request to the Flask backend.
3. The backend performs the DNS lookup.
4. The application displays the returned records and response time.
5. Cache statistics and lookup history help demonstrate DNS performance.
6. The trace visualization illustrates the conceptual DNS resolution stages.

## 8. Applications
- Learning DNS concepts in computer networks.
- Understanding domain-name resolution.
- Demonstrating DNS caching and lookup performance.
- Practicing frontend and backend integration.

## 9. Future Enhancements
- Add more DNS record types and diagnostic checks.
- Improve visualizations and error handling.
- Add advanced DNS security analysis.
- Support comparison of cached and uncached lookups.

## 10. Conclusion
DNS Insight provides an interactive way to explore DNS lookups, caching, response times, and resolution behavior. It combines networking concepts with web development to create a practical educational