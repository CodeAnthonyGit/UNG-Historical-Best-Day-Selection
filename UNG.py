import pandas as pd


#Best historical buy/sell combo:
#Buy Month: 12.0, Buy Day: 20.0
#Sell Month: 1.0, Sell Day: 11.0
#Average Return: 10.95%
#Median Return: 16.88%
#Percent Profitable: 80.0%
#Years Used: 5.0



# ------------------------------------------------
year5_excel = r"/Users/adrianchenoweth/Downloads/UNG Historical Trading.xlsx"
DATE_COL = "Date"
PRICE_COL = "Close"

buy_day = 20
buy_month = 12
sell_day = 11
sell_month = 1
# ------------------------------------------------

# ------------------------------------------------
df = pd.read_excel(year5_excel, nrows=265)
df.columns = df.columns.str.strip() 
df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
df = df.dropna(subset=[DATE_COL])
df = df.sort_values(DATE_COL).reset_index(drop=True)

df["Year"] = df[DATE_COL].dt.year
df["Month"] = df[DATE_COL].dt.month
df["Day"] = df[DATE_COL].dt.day
# ------------------------------------------------

# ------------------------------------------------
results = [] 

def returnp(buy, sell): 
    return ((sell - buy) / buy) * 100
# ------------------------------------------------

# ------------------------------------------------
for year in df["Year"].unique():
    buy_data = df[(df["Year"] == year) & (df["Month"] == buy_month) & (df["Day"] >= buy_day)]
    if buy_data.empty:
        continue
    buy_row = buy_data.iloc[0] #acces row and column, can switch to volaility calculation with open pricing as well vs month average using lin reg and noise
    buy_date = buy_row[DATE_COL]
    buy_price = buy_row[PRICE_COL]

    # sell for 100%, maybe try messing with ratio split to average daily returns and risk
    sell_data = df[(df["Year"] == year+1) & (df["Month"] == sell_month) & (df["Day"] <= sell_day)]
    if sell_data.empty:
        continue
    sell_row = sell_data.iloc[-1]
    sell_date = sell_row[DATE_COL]
    sell_price = sell_row[PRICE_COL]
    
    
    ret = returnp(buy_price, sell_price)
    
    results.append({
        "Year": year,
        "BuyDate": buy_date,
        "BuyPrice": buy_price,
        "SellDate": sell_date,
        "SellPrice": sell_price,
        "Return": ret
    })

res_df = pd.DataFrame(results)
# ------------------------------------------------

# % prof
pct_profitable = (res_df["Return"] > 0).mean() * 100
# mean return
avg_return = res_df["Return"].mean()
# median return
median_return = res_df["Return"].median()

print("Yearly strategy results:")
print(res_df)
print("\nSummary stats:")
print(f"Percent profitable: {pct_profitable:.1f}%")
print(f"Average return: {avg_return:.2f}%")
print(f"Median return: {median_return:.2f}%")

#if done with ranging over loop for days/month could create a probability distribution 
#res_df.to_csv("manual_strategy_results.csv", index=False)

