import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.write("App started")
st.title("WTG Power Curve Dashboard")
ref_wind = [
0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9,5,5.1,5.2,5.3,5.4,5.5,5.6,5.7,5.8,5.9,6,6.1,6.2,6.3,6.4,6.5,6.6,6.7,6.8,6.9,7,7.1,7.2,7.3,7.4,7.5,7.6,7.7,7.8,7.9,8,8.1,8.2,8.3,8.4,8.5,8.6,8.7,8.8,8.9,9,9.1,9.2,9.3,9.4,9.5,9.6,9.7,9.8,9.9,10,10.1,10.2,10.3,10.4,10.5,10.6,10.7,10.8,10.9,11,11.1,11.2,11.3,11.4,11.5,11.6,11.7,11.8,11.9,12,12.1,12.2,12.3,12.4,12.5,12.6,12.7,12.8,12.9,13,13.1,13.2,13.3,13.4,13.5,13.6,13.7,13.8,13.9,14,14.1,14.2,14.3,14.4,14.5,14.6,14.7,14.8,14.9,15,15.1,15.2,15.3,15.4,15.5,15.6,15.7,15.8,15.9,16,16.1,16.2,16.3,16.4,16.5,16.6,16.7,16.8,16.9,17,17.1,17.2,17.3,17.4,17.5,17.6,17.7,17.8,17.9,18
]

ref_power = [
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6.2,12.4,18.6,24.8,31,45,59,73,87,101,122,143,164,185,206,233.4,260.8,288.2,315.6,343,378.6,414.2,449.8,485.4,521,562,603,644,685,726,773.6,821.2,868.8,916.4,964,1019,1074,1129,1184,1239,1302.6,1366.2,1429.8,1493.4,1557,1629.6,1702.2,1774.8,1847.4,1920,1998.4,2076.8,2155.2,2233.6,2312,2380.2,2448.4,2516.6,2584.8,2653,2700.6,2748.2,2795.8,2843.4,2891,2918.4,2945.8,2973.2,3000.6,3028,3041.4,3054.8,3068.2,3081.6,3095,3101.8,3108.6,3115.4,3122.2,3129,3132.4,3135.8,3139.2,3142.6,3146,3146.8,3147.6,3148.4,3149.2,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150,3150

]
# Load data

@st.cache_data(ttl=120)
def load_data():
    df = pd.read_excel("DhMarch01to222026.xlsx")
    return df[['Source', 'Timestamp', 'AI_intern_Windspeed', 'AI_intern_ActivePower']]
df = load_data()

#df = pd.read_excel("DhMarch01to222026.xlsx")  # or your file

wind_col = 'AI_intern_Windspeed'
power_col = 'AI_intern_ActivePower'

# Sidebar filters
st.sidebar.header("Filters")

selected_turbine = st.sidebar.selectbox(
    "Select Turbine",
    df['Source'].unique()
)

# Optional: date filter
if 'Timestamp' in df.columns:
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    start_date = st.sidebar.date_input("Start Date", df['Timestamp'].min())
    end_date = st.sidebar.date_input("End Date", df['Timestamp'].max())
    
    df = df[(df['Timestamp'] >= pd.to_datetime(start_date)) &
            (df['Timestamp'] <= pd.to_datetime(end_date))]

# Filter data
df_filtered = df[df['Source'] == selected_turbine]

# Plot
fig, ax = plt.subplots(figsize=(8,5))

ax.scatter(
    df_filtered[wind_col],
    df_filtered[power_col],
    s=5,
    alpha=0.2
)

# Reference curve
ax.plot(
    ref_wind,
    ref_power,
    color='black',
    linewidth=2,
    linestyle='--'
)

ax.set_xlabel("Wind Speed")
ax.set_ylabel("Power")
ax.set_title(f"Power Curve - {selected_turbine}")
ax.grid()

st.pyplot(fig)








