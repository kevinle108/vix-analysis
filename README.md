# VIX Analysis

## Description:

The CBOE Volatility Index (VIX) is often used as a measurement of stock market fear and volatility. When VIX is high, it means people believe that the market is unstable. When VIX is low, people are more confident in the market's stability. I wanted to see how well the VIX correlates with the closing price of an index fund that tracks the S&P 500, such as VFIAX. This project is a console app that helps me analyze and visualize the historical daily percentage growth of VIX and VFIAX to better understand the correlation between the two.

## Setup Instructions:
- In the root project directory, create a virtual environment by running the command `python3 -m venv venv`
- Next activate the virtual environment by running:
  - `venv\Scripts\Activate.ps1` for Windows
  - `venv/bin/activate` for Unix/macOS
- Then install the project dependencies by running `pip install -r requirements.txt`
- Finally, run `python main.py` to start the console app.

## Notes: 
- Because there were too many data points when visualizing the historical growth of VIX vs VFIAX, I added visualizations for just this year (YTD). This smaller data set better visualizes the inverse correlation nature of VIX and VFIAX. And to see this relation even more clearly, there is a visualization of VIX-inverse vs VFIAX.

## Data Sources Used:
Downloaded from Yahoo Finance, the csv files `./data/historical/^VIX.csv` and `./data/historical/VFIAX.csv` were used to analyze the historical correlation of VIX and VFIAX . For the recent YTD visualizations, the program calls the Yahoo Finance API to collect this year's VIX and VFIAX data.

## Requirement features:
  - [x] Category 1: Python Programming Basics:
    - Implement a “master loop” console application where the user can repeatedly enter commands/perform actions, including choosing to exit the program.	
      - line 10 in `main.py` 
    - Create a dictionary or list, populate it with several values, retrieve at least one value, and use it in your program.
      - line 3 in `main.py`
    - Create and call at least 3 functions or methods, at least one of which must return a value that is used somewhere else in your code. 
      - lines 12, 15, 29, 63, 124, 133 in `analysis.py`
  - [x] Category 2: Utilize External Data:
    - Read data from an external file, such as text, JSON, CSV, etc, and use that data in your application.
      - line 36, 37 in `analysis.py`
    - Connect to an external/3rd party API and read data into your app
      - line 135 in `analysis.py`
  - [x] Category 3: Data Display:
    - Visualize data in a graph, chart, or other visual representation of data.
      - line 60 in `analysis.py`
  - [x] Category 4: Best Practices:
    - The program should utilize a virtual environment and document library dependencies in a requirements.txt file.
      - packages listed in `requirements.txt` file located in root directory
