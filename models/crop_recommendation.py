import pandas as pd

def recommend_crops(location, soil_type, land_size):
    crop_data = pd.read_csv('data/crop_data.csv')
    avg_prices = crop_data.groupby('Crop')['Price'].mean()
    recommendations = avg_prices.nlargest(5).reset_index()
    recommendations['Profit Level'] = recommendations['Price'].apply(lambda x: 'High' if x > avg_prices.mean() else 'Medium')
    recommendations['Demand Level'] = 'High'
    return recommendations[['Crop', 'Profit Level', 'Demand Level']].to_dict('records')