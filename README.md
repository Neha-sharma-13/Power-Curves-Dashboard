Wind Turbine Power Curve Dashboard
An interactive data analysis dashboard built using Streamlit to analyze and visualize wind turbine performance using SCADA data.

Project Overview
This project helps in analyzing Wind Turbine Generator (WTG) performance by comparing actual power output against expected behavior based on wind speed (power curve).

It enables:
Monitoring turbine efficiency
Detecting anomalies or underperformance
Visualizing power curves interactively

Features
Upload SCADA Excel data dynamically
Interactive power curve visualization (Wind Speed vs Power)
Data filtering and exploration
Fast data loading using caching
Clean and intuitive UI for analysis

Tech Stack
Python
Streamlit
Pandas
Matplotlib

Project Structure
power-curves-dashboard
-> app.py
─> requirements.txt
─> README.md

1. Clone the repository
git clone https://github.com/your-username/power-curves-dashboard.git
cd power-curves-dashboard
2. Install dependencies
pip install -r requirements.txt
3. Run the app
streamlit run app.py

How to Use :-
Launch the app
Upload your Excel file containing SCADA data
Explore wind speed vs power output and turbine performance
Data Requirements

Your Excel file should contain columns such as:
Source
Timestamp
AI_intern_Windspeed
AI_intern_ActivePower
Adjust based on your dataset.

Performance Optimization
Uses @st.cache_data for faster reloads
Recommended to use cleaned datasets for better performance

Author
Neha Sharma

License
This project is open-source and available under the MIT License.

Acknowledgements
Built using Streamlit and inspired by real-world wind energy analytics use cases.
