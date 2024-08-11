# Pinterest Web Scraper

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/0/08/Pinterest-logo.png" alt="Pinterest Logo" width="150">
</p>

## Overview

The **Pinterest Web Scraper** is a Python-based tool designed to download publicly saved pins from a given user's Pinterest account. The scraper navigates through a user's Pinterest boards and downloads images from their publicly accessible pins. This tool is intended for educational purposes or personal use only, and users must ensure they are complying with Pinterest's Terms of Service when using it.

## Features

- 🚀 **Scrape Public Pins**: Download all images from a specified Pinterest user's publicly saved pins.
- 📋 **Board-specific Scraping**: Option to scrape pins from specific boards instead of the entire account.
- 📁 **Customizable Output**: Save downloaded pins to a specified directory.
- 🛡️ **Error Handling**: Handles common issues such as rate limiting and inaccessible pins.

## Requirements

- Python 3.2
- Required Python packages:
  - `requests`
  - `beautifulsoup4`
  - `selenium`
  - `webdriver_manager`

You can install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Setup

1. Clone the repository
```bash
git clone https://github.com/AJM-L/PinterestScraper.git
cd PinterestScraper
```

2. Install dependancies
```bash
pip install -r requirements.txt
```

## Usage

- Run the DownloadAccount.py file
```bash
python DownloadAccount.py
```

- Input Account information when prompted
    - The program will ask for the account name and confirmation of the url
    - make sure the url is correct and if it is not resubmit with the correct account url

- Retrieve downloads
    - After all information has been given, the program will download the account pictures to the downloads folder