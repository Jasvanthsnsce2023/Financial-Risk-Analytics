import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read stock data
data = pd.read_csv("data/apple_stock.csv")

# Remove extra rows added by yfinance CSV format
data = data.iloc[2:].copy()

# Convert Close column to numeric
data["Close"] = pd.to_numeric(data["Close"])

# Calculate Daily Returns
data["Daily_Return"] = data["Close"].pct_change()

# Calculate Average Return and Risk
average_return = data["Daily_Return"].mean()
risk = data["Daily_Return"].std()

print("Average Daily Return:", average_return)
print("Risk (Volatility):", risk)

# Monte Carlo Simulation Settings
days = 252
simulations = 1000

last_price = data["Close"].iloc[-1]

simulation_df = pd.DataFrame()

# Run Simulations
for i in range(simulations):

    prices = [last_price]

    for d in range(days):

        future_return = np.random.normal(
            average_return,
            risk
        )

        next_price = prices[-1] * (1 + future_return)

        prices.append(next_price)

    simulation_df[i] = prices

# Final simulated prices
final_prices = simulation_df.iloc[-1]

print("\nExpected Future Price:",
      final_prices.mean())

print("\nBest Case Price:",
      final_prices.max())

print("\nWorst Case Price:",
      final_prices.min())

confidence_95 = np.percentile(
    final_prices,
    5
)

print("\n95% Confidence Price:",
      confidence_95)

# Create Risk Report
report = pd.DataFrame({
    "Metric": [
        "Average Daily Return",
        "Risk (Volatility)",
        "Expected Future Price",
        "Best Case Price",
        "Worst Case Price",
        "95% Confidence Price"
    ],
    "Value": [
        average_return,
        risk,
        final_prices.mean(),
        final_prices.max(),
        final_prices.min(),
        confidence_95
    ]
})

# Save Excel Report
report.to_excel(
    "output/risk_report.xlsx",
    index=False
)

print("\nRisk report saved successfully!")

# Save Simulation Graph
plt.figure(figsize=(10, 6))
plt.plot(simulation_df)

plt.title("Monte Carlo Simulation")
plt.xlabel("Days")
plt.ylabel("Predicted Stock Price")

plt.savefig(
    "output/monte_carlo_simulation.png"
)

plt.show()