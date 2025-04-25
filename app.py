from flask import Flask, render_template, request, redirect, url_for, flash
from utils.authentication import login_user, signup_user
from models.crop_price_prediction import predict_prices
from models.crop_recommendation import recommend_crops
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Home Page
@app.route('/')
def home():
    crop_data = pd.read_csv('data/crop_data.csv')
    avg_prices = crop_data.groupby('Crop')['Price'].mean().head(5).reset_index()
    return render_template('home.html', avg_prices=avg_prices)

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if login_user(username, password, role):
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')

# Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        location = request.form['location']
        if signup_user(name, username, password, role, location):
            flash('Signup successful!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists!', 'danger')
    return render_template('signup.html')

# Crop Price Prediction
@app.route('/predict', methods=['GET', 'POST'])
def crop_price_prediction():
    if request.method == 'POST':
        crop = request.form['crop']
        location = request.form['location']
        predictions, months = predict_prices(crop, location)
        return render_template('crop_price.html', crop=crop, location=location, predictions=predictions, months=months)
    return render_template('crop_price.html')

# Crop Recommendation
@app.route('/recommend', methods=['GET', 'POST'])
def crop_recommendation():
    if request.method == 'POST':
        location = request.form['location']
        soil_type = request.form['soil_type']
        land_size = float(request.form['land_size'])
        recommendations = recommend_crops(location, soil_type, land_size)
        return render_template('recommendation.html', recommendations=recommendations)
    return render_template('recommendation.html')

# Crop Marketplace
@app.route('/marketplace', methods=['GET', 'POST'])
def marketplace():
    if request.method == 'POST':
        crop = request.form['crop']
        quantity = request.form['quantity']
        contact = request.form['contact']
        location = request.form['location']
        company_posts = pd.read_csv('data/company_posts.csv')
        company_posts = company_posts.append({'Crop': crop, 'Quantity': quantity, 'Contact': contact, 'Location': location}, ignore_index=True)
        company_posts.to_csv('data/company_posts.csv', index=False)
        flash('Post added successfully!', 'success')
    company_posts = pd.read_csv('data/company_posts.csv')
    return render_template('marketplace.html', company_posts=company_posts)

if __name__ == '__main__':
    app.run(debug=True)