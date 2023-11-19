import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def load_data():
    # Load the dataset
    data = pd.read_csv('Medical_insurance.csv')  
    return data

def preprocess_data(data):
    # Convert categorical variables into dummy/indicator variables
    data = pd.get_dummies(data, columns=['sex', 'smoker', 'region'], drop_first=True)
    return data

def train_model(data):
    # Define features (X) and target variable (y)
    X = data.drop('charges', axis=1)
    y = data['charges']

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a Linear Regression model
    model = LinearRegression()

    # Train the model
    model.fit(X_train, y_train)

    return model

def main():
    st.title('Insurance Price Prediction App')

    # Load data
    data = load_data()

    # Preprocess data
    data = preprocess_data(data)

    # Train model
    model = train_model(data)

    st.sidebar.header('User Input Features')

    # Collect user inputs
    age = st.sidebar.slider('Age', min_value=18, max_value=64, value=25)
    bmi = st.sidebar.slider('BMI', min_value=15.0, max_value=50.0, value=25.0)
    children = st.sidebar.slider('Number of Children', min_value=0, max_value=5, value=0)
    sex_male = st.sidebar.checkbox('Male')
    smoker_yes = st.sidebar.checkbox('Smoker')
    region_northwest = st.sidebar.checkbox('Northwest')
    region_southeast = st.sidebar.checkbox('Southeast')
    region_southwest = st.sidebar.checkbox('Southwest')

    # Make a prediction
    input_data = pd.DataFrame({
        'age': [age],
        'bmi': [bmi],
        'children': [children],
        'sex_male': [1 if sex_male else 0],
        'smoker_yes': [1 if smoker_yes else 0],
        'region_northwest': [1 if region_northwest else 0],
        'region_southeast': [1 if region_southeast else 0],
        'region_southwest': [1 if region_southwest else 0],
    })

    # Reorder columns to match the order in the training data
    input_data = input_data[data.drop('charges', axis=1).columns]

    prediction = model.predict(input_data)

    st.subheader('Prediction')
    st.write(f'The predicted insurance charge is: {prediction[0]:.2f} USD')

if __name__ == '__main__':
    main()
