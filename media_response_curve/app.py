import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---- FUNCTIONS ----

def compute_adstock_series(spend_series, half_life):
    decay = 0.5 ** (1 / half_life)
    adstocked = []
    carryover = 0
    for spend in spend_series:
        current = spend + decay * carryover
        adstocked.append(current)
        carryover = current
    return np.array(adstocked)

def saturation_function(adstocked_spend, penetration, p=0.5):
    return (adstocked_spend ** p) / (adstocked_spend ** p + penetration ** p)

def compute_response_series(spend_series, half_life, penetration, effectiveness, p=0.5):
    adstocked = compute_adstock_series(spend_series, half_life)
    saturated = saturation_function(adstocked, penetration, p)
    response = effectiveness * saturated
    return response, adstocked

def compute_elasticity(response, adstocked):
    dy = np.gradient(response, adstocked)
    with np.errstate(divide='ignore', invalid='ignore'):
        elasticity = np.where(response != 0, dy * (adstocked / response), 0)
    return dy, elasticity

# ---- STREAMLIT UI ----

st.set_page_config(page_title="📈 Response Curve Tool", layout="wide")
st.title("🎯 Media Response Curve by Campaign")

st.markdown("""
Upload your **media spend data** and visualize how **response curves** behave with different parameters.

**Required CSV columns**:
- `Campaign` (string)
- `Spend` (numeric)
- Optional: `Date`, `Sales`
""")

with st.sidebar:
    st.header("📥 Upload CSV File")
    uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])

    st.header("🔧 Model Parameters")
    half_life = st.number_input("Half-life (days)", min_value=0.1, max_value=100.0, value=7.0, step=0.1)
    penetration = st.number_input("Penetration (₹)", min_value=1.0, max_value=1_000_000.0, value=2000.0, step=100.0)
    effectiveness = st.number_input("Effectiveness (units)", min_value=1.0, max_value=100_000.0, value=500.0, step=50.0)
    hill_power = st.number_input("Hill Exponent (curve steepness)", min_value=0.1, max_value=5.0, value=0.5, step=0.1)

# ---- MAIN APP ----

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    required_cols = {'Campaign', 'Spend'}
    if not required_cols.issubset(df.columns):
        st.error("CSV must contain at least 'Campaign' and 'Spend' columns.")
    else:
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df.sort_values(by=['Campaign', 'Date'], inplace=True)
        else:
            df['Date'] = pd.RangeIndex(len(df))  # fallback index

        campaign_list = df['Campaign'].unique().tolist()
        selected_campaign = st.selectbox("🎯 Select Campaign", campaign_list)

        # Filter data
        df_campaign = df[df['Campaign'] == selected_campaign].copy()
        df_campaign.sort_values('Date', inplace=True)

        # Compute model response
        response, adstocked = compute_response_series(
            df_campaign['Spend'], half_life, penetration, effectiveness, p=hill_power
        )
        df_campaign['Adstocked Spend'] = adstocked
        df_campaign['Model Response'] = response

        # Compute slope and elasticity
        slope, elasticity = compute_elasticity(response, adstocked)
        df_campaign['Slope (dy/dx)'] = slope
        df_campaign['Elasticity'] = elasticity

        # ---- POINTS A, C, D ----
        # A: Inflection Point (adstock ≈ penetration)
        point_A_x = penetration
        point_A_y = effectiveness * (point_A_x ** hill_power / (point_A_x ** hill_power + penetration ** hill_power))

        # C: Diminishing Return (slope < 50% of max)
        slope_threshold = slope.max() * 0.5
        idx_C = np.where(slope < slope_threshold)[0][0]
        point_C_x = adstocked[idx_C]
        point_C_y = response[idx_C]

        # D: Saturation Point (slope < 0.01)
        idx_D = np.where(slope < 0.01)[0][0]
        point_D_x = adstocked[idx_D]
        point_D_y = response[idx_D]

        # ---- PLOT ----
        st.subheader(f"📈 Response Curve: `{selected_campaign}`")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

        # --- RC Curve ---
        ax1.plot(adstocked, response, label="Model Response", color="green", linewidth=2)
        ax1.scatter([point_A_x, point_C_x, point_D_x], [point_A_y, point_C_y, point_D_y],
                    color=['orange', 'purple', 'red'], s=80, label="Points A, C, D")

        ax1.text(point_A_x, point_A_y, 'A: Inflection', color='orange', fontsize=9, ha='right')
        ax1.text(point_C_x, point_C_y, 'C: Diminishing', color='purple', fontsize=9, ha='right')
        ax1.text(point_D_x, point_D_y, 'D: Saturation', color='red', fontsize=9, ha='right')

        ax1.set_ylabel("Model Response")
        ax1.set_title("📊 Response Curve with A, C, D")
        ax1.grid(True)
        ax1.legend()

        # --- Elasticity & Slope ---
        ax2.plot(adstocked, slope, label="Marginal Slope (dY/dX)", color="blue")
        ax2.plot(adstocked, elasticity, label="Elasticity", color="red")
        ax2.axhline(1.0, linestyle='--', color='gray', label="Elasticity = 1")
        ax2.set_xlabel("Adstocked Spend")
        ax2.set_ylabel("Value")
        ax2.set_title("📉 Slope and Elasticity")
        ax2.grid(True)
        ax2.legend()

        st.pyplot(fig)
        
        #----- recccomendation about elasticity
        avg_elasticity = df_campaign['Elasticity'].mean()
        st.metric("📊 Average Elasticity", f"{avg_elasticity:.2f}")
        if avg_elasticity > 1:
            st.success("🔼 High Elasticity: Consider increasing media spend.")
        elif avg_elasticity > 0.8:
            st.info("✅ Good Elasticity: Maintain or slightly increase spend.")
        elif avg_elasticity > 0.5:
            st.warning("⚠️ Moderate Elasticity: Spend cautiously. Test optimizations.")
        elif avg_elasticity > 0.1:
            st.error("🔻 Low Elasticity: Response is inefficient. Consider reducing spend.")
        else:
            st.error("🛑 Saturation Zone: Stop or reallocate budget.")      
        # ---- TABLE ----
        with st.expander("📊 Show Data Table"):
            st.dataframe(df_campaign[['Date', 'Spend', 'Adstocked Spend', 'Model Response', 'Slope (dy/dx)', 'Elasticity']])
else:
    st.info("Please upload a CSV file to get started.")
