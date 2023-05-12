# Charts and KPIs

## Problem Statement
Design a dashboard to display the statistic of COVID19 cases. You are tasked to display one of the components of the dashboard which is to display a visualisation representation of number of COVID19 cases in Singapore over time.
- Data source:  public data from https://documenter.getpostman.com/view/10808728/SzS8rjbc#b07f97ba-24f4-4ebe-ad71-97fa35f3b683.

## Dashboard Design

![dashboard.png](/images/dashboard.png)

- A interactive dashboard is designed to show the number of COVID-19 cases over time in Singapore using the Dash framework in Python.
- The data is pulled using the APIs from https://covid19api.com/. 
- At first run, the data will be pulled from 1st Jan 2022 to 1st Jan 2023.
- Users can then change the From and To timestamp to dynamically update the graph.

## Usage
1. Install the required python packages.
```bash
pip install -r requirements.txt
```

2. Execute the python script
```bash
cd src
python -m run_dashboard
```
Expected output:
```
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'run_dashboard' (lazy loading)
...
```

3. Open the [localhost](http://127.0.0.1:8050/) to view the dashboard.
