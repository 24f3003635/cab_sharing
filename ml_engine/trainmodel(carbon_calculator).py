import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import numpy as np
import warnings 
warnings.filterwarnings("ignore")
print("🚀 Starting TransitCore ML Engine...")


print("📊 Generating synthetic traffic data...")
np.random.seed(42)
num_samples = 5000


hours = np.random.randint(0, 24, num_samples)
is_weekend = np.random.randint(0, 2, num_samples)
is_raining = np.random.randint(0, 2, num_samples)


traffic_multiplier = np.ones(num_samples)

for i in range(num_samples):
    
    if is_weekend[i] == 0 and ((8 <= hours[i] <= 10) or (17 <= hours[i] <= 19)):
        traffic_multiplier[i] += np.random.uniform(0.4, 0.8) 
    
    elif 11 <= hours[i] <= 16:
        traffic_multiplier[i] += np.random.uniform(0.1, 0.3)
        
    
    if is_raining[i] == 1:
        traffic_multiplier[i] += np.random.uniform(0.15, 0.35)


df = pd.DataFrame({
    'hour': hours,
    'is_weekend': is_weekend,
    'is_raining': is_raining,
    'traffic_multiplier': traffic_multiplier
})


df.to_csv("synthetic_traffic_data.csv", index=False)
print(" Saved 'synthetic_traffic_data.csv' (5000 rows)")


X = df[['hour', 'is_weekend', 'is_raining']]
y = df['traffic_multiplier']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
model.fit(X_train, y_train)


predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f"mean_squared_error{mse:.4f}")
joblib.dump(model,"traffic_model.joblib")




hour=int(input("enter the hours 1 to 11 for am and 12 to 23 for pm "))
raining=int(input("is it raining:0 for no 1 for yes"))
weekend=int(input("is it weekend:0 for no 1 for yes"))
user_input=np.array([[hour,weekend,raining]])
predictions=model.predict(user_input)[0]
print(predictions)

