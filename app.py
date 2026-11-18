import streamlit as st
import pandas as pd
import joblib
import time
import matplotlib.pyplot as plt

# page config
st.set_page_config(
    page_title="AI Dynamic Pricing",
    page_icon="💰",
    layout="centered"
)

# load model
model = joblib.load("pricing_model.pkl")

# session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# CSS styling
st.markdown("""
<style>

.stApp {
background: linear-gradient(135deg,#eef2ff,#ffffff);
font-family: 'Segoe UI';
}

.login-card {
background:white;
padding:35px;
border-radius:18px;
box-shadow:0 8px 30px rgba(0,0,0,0.15);
text-align:center;
}

.main-title {
text-align:center;
font-size:42px;
font-weight:700;
color:#1a237e;
}

.subtitle {
text-align:center;
color:#5c6bc0;
margin-bottom:20px;
}

.glass-card {
background: rgba(255,255,255,0.75);
padding:30px;
border-radius:18px;
box-shadow:0 8px 32px rgba(31,38,135,0.15);
margin-bottom:20px;
}

.result-card {
background: linear-gradient(135deg,#1a73e8,#42a5f5);
padding:35px;
border-radius:18px;
text-align:center;
color:white;
font-size:32px;
font-weight:600;
box-shadow:0 10px 30px rgba(0,0,0,0.15);
}

</style>
""", unsafe_allow_html=True)

# LOGIN PAGE
if not st.session_state.logged_in:

    st.markdown('<div class="main-title">🔐 Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI Dynamic Pricing System</div>', unsafe_allow_html=True)

    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_button = st.button("Login")

    st.markdown('</div>', unsafe_allow_html=True)

    if login_button:

        # simple login
        if username == "admin" and password == "1234":

            st.success("Login successful")

            progress = st.progress(0)

            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)

            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("Invalid username or password")

# MAIN APP
else:

    st.markdown('<div class="main-title">💰 AI Dynamic Pricing</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Smart Price Recommendation using Machine Learning</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        product_category = st.selectbox(
            "Product Category",
            ["Electronics","Clothing","Groceries","Furniture"]
        )

        discount = st.text_input("Discount %")

    with col2:

        marketing_spend = st.text_input("Marketing Spend")

        units_sold = st.text_input("Units Sold")

    predict_button = st.button("Predict Price")

    st.markdown('</div>', unsafe_allow_html=True)

    category_map = {
        "Electronics":0,
        "Clothing":1,
        "Groceries":2,
        "Furniture":3
    }

    if predict_button:

        try:

            input_data = {
                "Product_Category": category_map[product_category],
                "Discount": float(discount),
                "Marketing_Spend": float(marketing_spend),
                "Units_Sold": float(units_sold)
            }

            df = pd.DataFrame([input_data])

            prediction = model.predict(df)

            st.markdown(
                f'<div class="result-card">Recommended Price<br>₹ {prediction[0]:.2f}</div>',
                unsafe_allow_html=True
            )

            # chart
            x = [50,100,150,200,250]

            y = [
                model.predict(pd.DataFrame([{
                    "Product_Category":category_map[product_category],
                    "Discount":float(discount),
                    "Marketing_Spend":float(marketing_spend),
                    "Units_Sold":i
                }]))[0] for i in x
            ]

            plt.figure()
            plt.plot(x,y)
            plt.xlabel("Units Sold")
            plt.ylabel("Predicted Price")

            st.pyplot(plt)

        except:
            st.error("Please enter valid numeric values")

    # logout button
    if st.button("Logout"):

        st.session_state.logged_in = False
        st.rerun()

    st.markdown("---")
    st.caption("Machine Learning Model • Random Forest • Secure Login")