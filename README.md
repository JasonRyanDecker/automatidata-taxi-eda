# 🚕 2017 NYC Yellow Taxi — EDA Project
**Python · Pandas · Matplotlib | automatidata_project.py**

---

## About This Project

This was built as a hands-on assignment for the **Google Advanced Data Analytics Certificate** on Coursera.
The course walks you through real-world data workflows using Python, and this project was part of that curriculum.

If you're taking the same course and want access to the dataset, you can find it through the course materials directly:
👉 [Google Advanced Data Analytics Certificate — Coursera](https://www.coursera.org/professional-certificates/google-advanced-data-analytics)

---

## What This Is

I grabbed a dataset of 4,688 NYC Yellow Taxi trips from 2017 and dug into it.
The goal wasn't anything fancy — I wanted to practice the full EDA workflow:
load it, understand it, clean it, and actually visualize what's going on in a way
that makes sense to someone who's never seen the data before.

---

## Step 1 — Load the Data

Read the CSV into pandas and ran the basics to see what I was dealing with.

| Action | Code / Result |
|---|---|
| Load CSV | `df = pd.read_csv('2017_Yellow_Taxi_Trip_Data.csv')` |
| Check shape | `df.shape` → **(4688, 18)** |
| Check types | `df.dtypes` |
| Check nulls | `df.isnull().sum()` |
| Preview rows | `df.head(10)` |
| Summary stats | `df.describe()` |

---

## Step 2 — Clean the Data

Found a few issues right away. Fixed all of them before touching the analysis.

| Issue Found | Fix Applied |
|---|---|
| Datetime cols stored as strings | `pd.to_datetime()` on pickup & dropoff columns |
| 1 row with null values | `df.dropna(inplace=True)` |
| Negative fare/total amounts | `df = df[df['fare_amount'] >= 0]` |
| Unnamed index column | `df.drop(columns=['Unnamed: 0'])` |
| Bad trip durations (< 1m or > 3h) | Filtered after creating `trip_duration_min` |

**Rows after cleaning: 4,688 → 4,625**

---

## Step 3 — Feature Engineering

Built some new columns from what was already there — made the analysis a lot richer.

| New Column | How It Was Made |
|---|---|
| `trip_duration_min` | `(dropoff - pickup).dt.total_seconds() / 60` |
| `pickup_hour` | `tpep_pickup_datetime.dt.hour` |
| `pickup_weekday` | `tpep_pickup_datetime.dt.day_name()` |
| `tip_pct` | `(tip_amount / fare_amount) * 100` |
| `payment_label` | Mapped `payment_type` int → readable label |

---

## Step 4 — Visualize

Six charts saved to `taxi_dashboard.png` using a 2×3 matplotlib grid.

| Chart | What It Shows |
|---|---|
| Fare Amount Distribution | Histogram — most trips cost $5–$20, median marked |
| Trip Distance Distribution | Histogram — majority of rides are under 5 miles |
| Trips by Hour of Day | Bar chart — peaks at morning & evening rush hours |
| Trips by Day of Week | Bar chart — weekday vs weekend, Sat/Sun highlighted |
| Tip % by Payment Type | Bar chart — credit card tips way higher than cash |
| Fare vs Trip Distance | Scatter + trend line — roughly $2/mile |

---

## What I Found

- Median fare was **$11.76**, ranging from $0 to $152.30
- Most trips were short — median distance under 3 miles
- Demand peaked at **8–9am** and **6–7pm** (classic rush hour)
- Credit card riders tipped way more than cash payers
- Fare scales pretty linearly with distance at around **$2/mile**
- Weekday trips slightly outnumbered weekend ones

---

## How to Run It

```bash
# Clone the repo
git clone https://github.com/JasonRyanDecker/automatidata-taxi-eda.git
cd automatidata-taxi-eda

# Set up environment
python3 -m venv my_pandas_env
source my_pandas_env/bin/activate

# Install dependencies
pip install pandas numpy matplotlib

# Run
python3 automatidata_clean_viz.py
```

Output: `taxi_dashboard.png` saved to your project folder.

---

## Files

```
automatidata-taxi-eda/
├── README.md
├── .gitignore
├── automatidata_project.py      # initial EDA exploration
├── automatidata_clean_viz.py    # cleaning + all 6 charts
└── taxi_dashboard.png           # output visualization
```

> The CSV isn't included (too large for GitHub). The dataset is provided through the course materials —
> if you're enrolled, you'll find it there.
> 👉 [Google Advanced Data Analytics Certificate — Coursera](https://www.coursera.org/professional-certificates/google-advanced-data-analytics)

---

## Tools Used

`Python 3` · `Pandas` · `NumPy` · `Matplotlib` · `Ubuntu 24` · `Git`