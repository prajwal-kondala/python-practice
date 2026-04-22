import streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings("ignore")

# =============================================
# Page Configuration
# =============================================
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# =============================================
# Load Model and Scaler
# Streamlit Rule 5 — always @st.cache_resource!
# =============================================
@st.cache_resource
def load_model():
    model_path  = os.path.join(os.path.dirname(__file__), 
                               "house_price_model.pkl")
    scaler_path = os.path.join(os.path.dirname(__file__), 
                               "scaler.pkl")
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    return model, scaler

model, scaler = load_model()

# =============================================
# Header
# =============================================
st.title("🏠 California House Price Predictor")
st.markdown("""
**Built with Linear Regression — NumPy Scratch + sklearn**  
*Week 9 Learning Exercise | Prajwal Kondala | IIT KGP*
""")
st.divider()

# =============================================
# Sidebar — Model Info
# =============================================
with st.sidebar:
    st.header("📊 Model Info")
    st.metric("Model", "Linear Regression")
    st.metric("Training Houses", "16,512")
    st.metric("R² Score", "0.5758")
    st.metric("Avg Error", "$74,560")
    st.divider()
    st.markdown("""
    **What this model learned:**
    - Median income drives price most!
    - Location (Lat/Long) is very important!
    - Population barely affects price!
    """)
    st.divider()
    st.markdown("""
    **Three methods compared:**
    - NumPy Scratch R² = 0.5672
    - Normal Equation R² = 0.5758  
    - sklearn R² = 0.5758
    """)

# =============================================
# Main Layout
# =============================================
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🔧 Enter House Details")
    
    med_inc = st.slider(
        "Median Income (in $10,000s)",
        min_value=0.5, max_value=15.0,
        value=3.87, step=0.1,
        help="Median income of the neighborhood"
    )
    
    house_age = st.slider(
        "House Age (years)",
        min_value=1, max_value=52,
        value=29, step=1
    )
    
    ave_rooms = st.slider(
        "Average Rooms per House",
        min_value=1.0, max_value=15.0,
        value=5.4, step=0.1
    )
    
    ave_bedrms = st.slider(
        "Average Bedrooms per House",
        min_value=0.5, max_value=5.0,
        value=1.1, step=0.1
    )
    
    population = st.slider(
        "Block Population",
        min_value=100, max_value=5000,
        value=1425, step=50
    )
    
    ave_occup = st.slider(
        "Average Occupancy",
        min_value=1.0, max_value=10.0,
        value=3.07, step=0.1
    )
    
    latitude = st.slider(
        "Latitude",
        min_value=32.0, max_value=42.0,
        value=35.6, step=0.1
    )
    
    longitude = st.slider(
        "Longitude",
        min_value=-125.0, max_value=-114.0,
        value=-119.6, step=0.1
    )

with col2:
    st.header("🎯 Prediction Result")
    
    # Prepare input for prediction
    input_features = np.array([[
        med_inc, house_age, ave_rooms, ave_bedrms,
        population, ave_occup, latitude, longitude
    ]])
    
    # Scale using saved scaler
    input_scaled = scaler.transform(input_features)
    
    # Predict
    prediction = model.predict(input_scaled)[0]
    price_usd = prediction * 100000
    
    # Display prediction
    st.metric(
        label="Predicted House Price",
        value=f"${price_usd:,.0f}",
        delta=f"Raw value: {prediction:.3f}"
    )
    
    st.divider()
    
    # Price category
    if prediction < 1.5:
        category = "🟢 Budget Friendly (under $150K)"
    elif prediction < 2.5:
        category = "🟡 Mid Range ($150K - $250K)"
    elif prediction < 4.0:
        category = "🟠 Premium ($250K - $400K)"
    else:
        category = "🔴 Luxury ($400K+)"
    
    st.markdown(f"**Category:** {category}")
    
    st.divider()
    
    # Feature importance chart
    st.subheader("📈 What Drives This Price?")
    
    feature_names = ['MedInc', 'HouseAge', 'AveRooms',
                     'AveBedrms', 'Population', 'AveOccup',
                     'Latitude', 'Longitude']
    coefficients = model.coef_
    
    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ['green' if c > 0 else 'red' 
              for c in coefficients]
    ax.barh(feature_names, coefficients, 
            color=colors, alpha=0.7, edgecolor='black')
    ax.axvline(x=0, color='black', linewidth=1)
    ax.set_title('Feature Importance\n'
                 'Green = raises price | Red = lowers price')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

# =============================================
# Bottom Section — Learning Summary
# =============================================
st.divider()
st.header("📚 What This Project Taught")

col3, col4, col5 = st.columns(3)

with col3:
    st.markdown("""
    **NumPy Scratch**
    - Implemented gradient descent manually
    - 1000 epochs → cost 2.63 → 0.29
    - 89% error reduction!
    - R² = 0.5672
    """)

with col4:
    st.markdown("""
    **Normal Equation**
    - θ = (XᵀX)⁻¹ Xᵀy
    - Exact solution in ONE step!
    - No epochs, no learning rate
    - R² = 0.5758
    """)

with col5:
    st.markdown("""
    **sklearn**
    - Uses Normal Equation internally
    - Identical to Normal Equation!
    - One line: model.fit()
    - R² = 0.5758
    """)

# Footer
st.divider()
st.markdown("""
*Week 9 Learning Exercise*  
*Prajwal Kondala | IIT KGP → AI/ML Engineer | April 2026*  
*python-practice folder | Phase 2: ML Foundations*
""")