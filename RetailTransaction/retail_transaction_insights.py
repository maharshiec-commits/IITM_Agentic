"""
============================================================================
 RETAIL TRANSACTION INSIGHTS  (Graded Mini Project - Part B)
============================================================================

DESIGN NOTES / ASSUMPTIONS:

- Input file: 'Retail_Transactions_Dataset.csv' must be in the same folder
  as this script (or edit DATA_PATH below). Replace the sample file with
  your real, full dataset before submitting - the code itself does not
  change.
- The 'Product' column is stored as a string that LOOKS like a Python list,
  e.g. "['Ketchup', 'Shaving Cream', 'Light Bulbs']". We convert it back
  into a real list with ast.literal_eval so we can count individual
  products (needed for "top 5 products").
- 'Discount_Applied' arrives as the text TRUE/FALSE, so it is converted to
  a real boolean.
- 'Promotion' uses the literal text "None" to mean "no promotion" - this is
  kept as its own category ("No Promotion") rather than a NaN, so it can be
  grouped/plotted like any other promotion type.
- 'Date' is parsed as day-first (DD-MM-YYYY HH:MM) and Year / Month /
  MonthName / DayOfWeek are extracted as separate columns for the
  seasonality and monthly-trend analysis.
- All charts are saved as PNG files into ./charts/ AND shown, so they can
  be dropped straight into a report/PDF.
============================================================================
"""

import ast
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
DATA_PATH = "RetailTransaction\\Retail_Transactions_Dataset.csv"
CHART_DIR = "charts"
os.makedirs(CHART_DIR, exist_ok=True)

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (9, 5)


def save_and_show(fig, filename):
    """Save a figure to CHART_DIR and display it."""
    path = os.path.join(CHART_DIR, filename)
    fig.savefig(path, bbox_inches="tight", dpi=120)
    plt.show()
    print(f"  (chart saved to {path})")


def section(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


# ============================================================================
# TASK 1: DATA PREPARATION
# ============================================================================
def load_and_prepare(path=DATA_PATH):
    df = pd.read_csv(path)

    # --- Parse dates ---
    # The dataset has been seen in two formats: day-first "21-01-2022 06:27"
    # and ISO "2022-01-21 06:27:29". format="mixed" lets pandas infer the
    # correct format row-by-row instead of assuming one fixed pattern, so
    # either style (or a mix of both) parses correctly. dayfirst=True only
    # affects genuinely ambiguous cases (e.g. "01-02-2022"); ISO dates with
    # a 4-digit year first are unaffected.
    df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=True, errors="coerce")

    # --- Extract useful date parts ---
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["MonthName"] = df["Date"].dt.month_name()
    df["DayOfWeek"] = df["Date"].dt.day_name()

    # --- Convert Discount_Applied text to boolean ---
    df["Discount_Applied"] = (
        df["Discount_Applied"].astype(str).str.strip().str.upper().map(
            {"TRUE": True, "FALSE": False}
        )
    )

    # --- Treat the literal "None" promotion as its own clean category ---
    df["Promotion"] = df["Promotion"].fillna("No Promotion")
    df["Promotion"] = df["Promotion"].replace("None", "No Promotion")

    # --- Basic cleaning: drop exact duplicate rows, drop rows with no date ---
    # (done before adding the Product_List column below, since a column of
    # Python lists is unhashable and breaks drop_duplicates)
    before = len(df)
    df = df.drop_duplicates()
    df = df.dropna(subset=["Date"])
    after = len(df)
    if before != after:
        print(f"  Cleaning: removed {before - after} duplicate/invalid-date rows.")

    # --- Parse Product column from "['A', 'B']" string into a real list ---
    def parse_products(val):
        try:
            return ast.literal_eval(val)
        except (ValueError, SyntaxError):
            return []
    df["Product_List"] = df["Product"].apply(parse_products)

    # --- Make sure numeric columns are numeric ---
    df["Total_Items"] = pd.to_numeric(df["Total_Items"], errors="coerce")
    df["Total_Cost"] = pd.to_numeric(df["Total_Cost"], errors="coerce")

    return df


# ============================================================================
# TASK 2: BASIC EXPLORATION
# ============================================================================
def basic_exploration(df):
    section("TASK 2: BASIC EXPLORATION")

    total_transactions = len(df)
    unique_customers = df["Customer_Name"].nunique()
    print(f"Total transactions: {total_transactions}")
    print(f"Unique customers: {unique_customers}")

    # Top 5 most common products (explode the parsed product lists)
    all_products = df["Product_List"].explode()
    top_products = all_products.value_counts().head(5)
    print("\nTop 5 most common products:")
    print(top_products.to_string())

    # Cities with the highest number of transactions
    top_cities = df["City"].value_counts()
    print("\nCities ranked by number of transactions:")
    print(top_cities.to_string())

    return {
        "total_transactions": total_transactions,
        "unique_customers": unique_customers,
        "top_products": top_products,
        "top_cities": top_cities,
    }


# ============================================================================
# TASK 3: CUSTOMER BEHAVIOUR ANALYSIS
# ============================================================================
def customer_behaviour(df):
    section("TASK 3: CUSTOMER BEHAVIOUR ANALYSIS")

    # Average spend per customer category
    avg_spend_by_category = (
        df.groupby("Customer_Category")["Total_Cost"].mean().sort_values(ascending=False)
    )
    print("Average spend by customer category (highest first):")
    print(avg_spend_by_category.round(2).to_string())

    # Preferred payment method per customer category
    preferred_payment = (
        df.groupby("Customer_Category")["Payment_Method"]
        .agg(lambda s: s.value_counts().idxmax())
    )
    print("\nMost-used payment method per customer category:")
    print(preferred_payment.to_string())

    # Full cross-tab, useful to see if preference is a strong majority or a mild lean
    payment_crosstab = pd.crosstab(df["Customer_Category"], df["Payment_Method"])
    print("\nFull breakdown (counts):")
    print(payment_crosstab.to_string())

    # Average items bought per transaction, per store type
    avg_items_by_store = (
        df.groupby("Store_Type")["Total_Items"].mean().sort_values(ascending=False)
    )
    print("\nAverage items per transaction, by store type:")
    print(avg_items_by_store.round(2).to_string())

    return {
        "avg_spend_by_category": avg_spend_by_category,
        "preferred_payment": preferred_payment,
        "avg_items_by_store": avg_items_by_store,
    }


# ============================================================================
# TASK 4: PROMOTION & DISCOUNT IMPACT
# ============================================================================
def promotion_discount_impact(df):
    section("TASK 4: PROMOTION & DISCOUNT IMPACT")

    # Average cost: discount applied vs not
    avg_cost_by_discount = df.groupby("Discount_Applied")["Total_Cost"].mean()
    print("Average transaction cost - Discount applied vs not:")
    print(avg_cost_by_discount.round(2).to_string())

    # Average items purchased per promotion type
    avg_items_by_promo = (
        df.groupby("Promotion")["Total_Items"].mean().sort_values(ascending=False)
    )
    print("\nAverage items purchased, by promotion type:")
    print(avg_items_by_promo.round(2).to_string())

    # Most effective promotion in terms of total cost
    avg_cost_by_promo = (
        df.groupby("Promotion")["Total_Cost"].mean().sort_values(ascending=False)
    )
    print("\nAverage transaction cost, by promotion type (most effective first):")
    print(avg_cost_by_promo.round(2).to_string())
    best_promo = avg_cost_by_promo.index[0]
    print(f"\n-> Most effective promotion by average spend: '{best_promo}'")

    return {
        "avg_cost_by_discount": avg_cost_by_discount,
        "avg_items_by_promo": avg_items_by_promo,
        "avg_cost_by_promo": avg_cost_by_promo,
        "best_promo": best_promo,
    }


# ============================================================================
# TASK 5: SEASONALITY TRENDS
# ============================================================================
def seasonality_trends(df):
    section("TASK 5: SEASONALITY TRENDS")

    # Total revenue by season
    revenue_by_season = df.groupby("Season")["Total_Cost"].sum().sort_values(ascending=False)
    print("Total revenue by season (highest first):")
    print(revenue_by_season.round(2).to_string())
    top_season = revenue_by_season.index[0]
    print(f"\n-> Highest-revenue season: {top_season}")

    # Seasonal preference for store types (counts)
    season_store_pref = pd.crosstab(df["Season"], df["Store_Type"])
    print("\nTransaction counts by Season vs Store Type:")
    print(season_store_pref.to_string())

    # Seasonal preference for products (top product per season)
    exploded = df[["Season", "Product_List"]].explode("Product_List")
    top_product_per_season = (
        exploded.groupby("Season")["Product_List"]
        .agg(lambda s: s.value_counts().idxmax() if len(s.dropna()) else None)
    )
    print("\nMost popular product per season:")
    print(top_product_per_season.to_string())

    # --- Plot: average spending per season ---
    avg_spend_by_season = df.groupby("Season")["Total_Cost"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots()
    avg_spend_by_season.plot(kind="bar", color="teal", ax=ax)
    ax.set_title("Average Spending per Season")
    ax.set_xlabel("Season")
    ax.set_ylabel("Average Total Cost")
    plt.xticks(rotation=0)
    save_and_show(fig, "avg_spending_per_season.png")
    plt.close(fig)

    return {
        "revenue_by_season": revenue_by_season,
        "season_store_pref": season_store_pref,
        "top_product_per_season": top_product_per_season,
        "avg_spend_by_season": avg_spend_by_season,
    }


# ============================================================================
# TASK 6: VISUALISATION DASHBOARD
# ============================================================================
def visualisation_dashboard(df):
    section("TASK 6: VISUALISATION DASHBOARD")

    # --- 1. Bar plot: number of transactions per city ---
    fig, ax = plt.subplots()
    df["City"].value_counts().plot(kind="bar", color="steelblue", ax=ax)
    ax.set_title("Number of Transactions per City")
    ax.set_xlabel("City")
    ax.set_ylabel("Transactions")
    plt.xticks(rotation=45, ha="right")
    save_and_show(fig, "transactions_per_city.png")
    plt.close(fig)

    # --- 2. Pie chart: distribution of payment methods ---
    fig, ax = plt.subplots()
    df["Payment_Method"].value_counts().plot(
        kind="pie", autopct="%1.1f%%", ax=ax, ylabel=""
    )
    ax.set_title("Payment Method Distribution")
    save_and_show(fig, "payment_method_distribution.png")
    plt.close(fig)

    # --- 3. Line chart: monthly revenue trend (grouped by year) ---
    monthly_revenue = (
        df.groupby(["Year", "Month"])["Total_Cost"].sum().reset_index()
    )
    fig, ax = plt.subplots()
    for year, grp in monthly_revenue.groupby("Year"):
        ax.plot(grp["Month"], grp["Total_Cost"], marker="o", label=str(int(year)))
    ax.set_title("Monthly Revenue Trend (by Year)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Revenue")
    ax.set_xticks(range(1, 13))
    ax.legend(title="Year")
    save_and_show(fig, "monthly_revenue_trend.png")
    plt.close(fig)

    # --- 4. Heatmap: revenue by season and customer category ---
    pivot = df.pivot_table(
        index="Season", columns="Customer_Category", values="Total_Cost", aggfunc="sum"
    ).fillna(0)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
    ax.set_title("Revenue by Season and Customer Category")
    save_and_show(fig, "revenue_season_vs_category_heatmap.png")
    plt.close(fig)


# ============================================================================
# SUMMARY OF KEY INSIGHTS
# ============================================================================
def print_summary(explore, behaviour, promo, season):
    section("SUMMARY OF KEY INSIGHTS")
    top_city = explore["top_cities"].index[0]
    top_product = explore["top_products"].index[0]
    top_spender_category = behaviour["avg_spend_by_category"].index[0]
    best_promo = promo["best_promo"]
    top_season = season["revenue_by_season"].index[0]

    discount_true = promo["avg_cost_by_discount"].get(True, float("nan"))
    discount_false = promo["avg_cost_by_discount"].get(False, float("nan"))

    print(f"""
- Dataset covers {explore['total_transactions']} transactions from
  {explore['unique_customers']} unique customers.
- '{top_product}' was the most frequently purchased product overall.
- '{top_city}' recorded the highest number of transactions.
- '{top_spender_category}' customers spend the most on average per
  transaction, suggesting this segment could be a priority for loyalty
  or premium offers.
- Transactions with a discount applied averaged {discount_true:.2f} vs
  {discount_false:.2f} without a discount, indicating {"discounts are associated with higher basket value" if discount_true > discount_false else "discounts alone do not increase average basket size"}.
- '{best_promo}' produced the highest average transaction value among all
  promotion types, making it the strongest candidate to run more often.
- '{top_season}' is the strongest-revenue season overall - marketing spend
  and inventory planning could be weighted toward this period.

(Note: these numeric insights reflect whichever CSV is in DATA_PATH. Re-run
this script after swapping in the full 'Retail_Transactions_Dataset.csv' to
get the real, submission-ready figures.)
""")


# ============================================================================
# ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    df = load_and_prepare()
    explore = basic_exploration(df)
    behaviour = customer_behaviour(df)
    promo = promotion_discount_impact(df)
    season = seasonality_trends(df)
    visualisation_dashboard(df)
    print_summary(explore, behaviour, promo, season)
