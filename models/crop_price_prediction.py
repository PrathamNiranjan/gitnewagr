import pandas as pd
from sklearn.linear_model import LinearRegression

def predict_prices(crop, location):
    crop_data = pd.read_csv('data/crop_data.csv')
    crop_data = crop_data[(crop_data['Crop'] == crop) & (crop_data['Location'] == location)]
    crop_data['Month_Year'] = pd.to_datetime(crop_data[['Year', 'Month']].assign(day=1))
    crop_data = crop_data.sort_values('Month_Year')
    X = crop_data[['Month_Year']].apply(lambda x: x.dt.toordinal())
    y = crop_data['Price']
    model = LinearRegression().fit(X, y)
    future_dates = pd.date_range(crop_data['Month_Year'].max(), periods=6, freq='MS')
    future_dates_ordinal = future_dates.to_series().apply(lambda x: x.toordinal()).values.reshape(-1, 1)
    predictions = model.predict(future_dates_ordinal)
    return predictions, future_dates.strftime('%B %Y').tolist()