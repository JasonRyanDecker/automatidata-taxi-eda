import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')

# ──────────────────────────────────────────────
# 1. LOAD
# ──────────────────────────────────────────────
df = pd.read_csv('2017_Yellow_Taxi_Trip_Data.csv')
print(f"✅ Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ──────────────────────────────────────────────
# 2. CLEAN
# ──────────────────────────────────────────────

# Show all columns
pd.set_option('display.max_columns', None)

# Convert datetimes
df['tpep_pickup_datetime']  = pd.to_datetime(df['tpep_pickup_datetime'])
df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

# Drop the 1 null row
before = len(df)
df.dropna(inplace=True)
print(f"🗑️  Dropped {before - len(df)} null row(s) → {len(df)} rows remain")

# Drop unnamed index column
df.drop(columns=['Unnamed: 0'], inplace=True)

# Remove negative fares / total amounts (refund artifacts)
df = df[(df['fare_amount'] >= 0) & (df['total_amount'] >= 0)]
print(f"🗑️  Removed negative fares → {len(df)} rows remain")

# Engineer useful columns
df['trip_duration_min'] = (
    df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']
).dt.total_seconds() / 60

df['pickup_hour']    = df['tpep_pickup_datetime'].dt.hour
df['pickup_weekday'] = df['tpep_pickup_datetime'].dt.day_name()

# Remove nonsensical durations (< 1 min or > 3 hours)
df = df[(df['trip_duration_min'] >= 1) & (df['trip_duration_min'] <= 180)]
print(f"🗑️  Removed bad durations → {len(df)} rows remain")

print("\n✅ Clean dataset preview:")
print(df[['VendorID','fare_amount','trip_distance',
          'trip_duration_min','pickup_hour','pickup_weekday']].head())

# ──────────────────────────────────────────────
# 3. VISUALIZE  (6 charts, 2×3 grid)
# ──────────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle('2017 NYC Yellow Taxi — Trip Insights', fontsize=18, fontweight='bold', y=1.01)
fig.patch.set_facecolor('#f7f7f7')

YELLOW  = '#F7C43B'
DARK    = '#1a1a2e'
ACCENT  = '#e63946'

# ── Chart 1: Fare amount distribution ──
ax = axes[0, 0]
ax.hist(df['fare_amount'], bins=40, color=YELLOW, edgecolor=DARK, linewidth=0.4)
ax.set_title('Fare Amount Distribution', fontweight='bold')
ax.set_xlabel('Fare ($)')
ax.set_ylabel('Number of Trips')
ax.axvline(df['fare_amount'].median(), color=ACCENT, linestyle='--', linewidth=1.5,
           label=f"Median: ${df['fare_amount'].median():.2f}")
ax.legend()
ax.set_facecolor('#fafafa')

# ── Chart 2: Trip distance distribution ──
ax = axes[0, 1]
dist = df[df['trip_distance'] < 20]   # focus on <20 miles (outliers excluded)
ax.hist(dist['trip_distance'], bins=40, color=DARK, edgecolor='white', linewidth=0.4)
ax.set_title('Trip Distance Distribution (< 20 mi)', fontweight='bold')
ax.set_xlabel('Distance (miles)')
ax.set_ylabel('Number of Trips')
ax.axvline(dist['trip_distance'].median(), color=YELLOW, linestyle='--', linewidth=1.5,
           label=f"Median: {dist['trip_distance'].median():.2f} mi")
ax.legend()
ax.set_facecolor('#fafafa')

# ── Chart 3: Trips by hour of day ──
ax = axes[0, 2]
hourly = df.groupby('pickup_hour').size()
ax.bar(hourly.index, hourly.values, color=YELLOW, edgecolor=DARK, linewidth=0.4)
ax.set_title('Trips by Hour of Day', fontweight='bold')
ax.set_xlabel('Hour (0 = midnight)')
ax.set_ylabel('Number of Trips')
ax.set_xticks(range(0, 24))
ax.set_facecolor('#fafafa')

# ── Chart 4: Trips by day of week ──
ax = axes[1, 0]
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
weekday = df['pickup_weekday'].value_counts().reindex(day_order)
colors = [ACCENT if d in ['Saturday','Sunday'] else DARK for d in day_order]
ax.bar(weekday.index, weekday.values, color=colors, edgecolor='white', linewidth=0.4)
ax.set_title('Trips by Day of Week', fontweight='bold')
ax.set_xlabel('Day')
ax.set_ylabel('Number of Trips')
ax.tick_params(axis='x', rotation=30)
ax.set_facecolor('#fafafa')

# ── Chart 5: Tip % by payment type ──
ax = axes[1, 1]
df['tip_pct'] = (df['tip_amount'] / df['fare_amount'].replace(0, np.nan)) * 100
payment_labels = {1: 'Credit Card', 2: 'Cash', 3: 'No Charge', 4: 'Dispute'}
df['payment_label'] = df['payment_type'].map(payment_labels).fillna('Other')
tip_by_payment = df.groupby('payment_label')['tip_pct'].median().sort_values(ascending=False)
ax.bar(tip_by_payment.index, tip_by_payment.values, color=YELLOW, edgecolor=DARK, linewidth=0.4)
ax.set_title('Median Tip % by Payment Type', fontweight='bold')
ax.set_xlabel('Payment Type')
ax.set_ylabel('Median Tip (%)')
ax.set_facecolor('#fafafa')

# ── Chart 6: Fare vs distance scatter ──
ax = axes[1, 2]
sample = df[df['trip_distance'] < 20].sample(min(1000, len(df)), random_state=42)
ax.scatter(sample['trip_distance'], sample['fare_amount'],
           alpha=0.3, s=15, color=DARK)
# Trend line
m, b = np.polyfit(sample['trip_distance'], sample['fare_amount'], 1)
x_line = np.linspace(0, 20, 100)
ax.plot(x_line, m * x_line + b, color=ACCENT, linewidth=2, label=f'Trend: ${m:.2f}/mi')
ax.set_title('Fare vs Trip Distance', fontweight='bold')
ax.set_xlabel('Distance (miles)')
ax.set_ylabel('Fare ($)')
ax.legend()
ax.set_facecolor('#fafafa')

plt.tight_layout()
plt.savefig('taxi_dashboard.png', dpi=150, bbox_inches='tight')
print("\n✅ Saved → taxi_dashboard.png")
plt.show()