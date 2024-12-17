# **PBA Scraper**

## **Overview**
This project is a web scraper that extracts basketball player and team information from the Philippine Basketball Association (PBA) website. The scraper efficiently retrieves data such as:

- Player Name
- Team Name
- Player Number
- Position
- Team Manager
- Head Coach

The script avoids unnecessary delays by extracting data directly from summary pages whenever possible.

---

## **Features**
- Extracts **player details**: Name, Team, Number, and Position.
- Extracts **team management details**: Head Coach and Team Manager.
- Handles unexpected HTML structures with robust error handling.
- Cleans up unwanted characters like double quotes in names.
- Optimized to minimize page requests for faster scraping.

---

## **Requirements**

Make sure you have the following installed:

- **Python 3.x**
- Required Python Libraries:
  - `requests`
  - `beautifulsoup4`

Install dependencies using:

```bash
pip install requests beautifulsoup4

## **Usage**

1. Setup
Ensure the script pba_scraper.py is in your working directory.

2. Run the Script
Execute the scraper using the command:

python pba_scraper.py

3. Outputs
Extracted player and team information will be displayed on the terminal.
The script can be modified to save data to a CSV or JSON file for further use.