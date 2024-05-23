import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import mean_squared_error, accuracy_score, confusion_matrix

# Load the original CSV file
log_data = pd.read_csv('StreamLit/preprocessed_web_logs.csv')

# Convert 'Date' and 'Time' columns to datetime objects
log_data['Date'] = pd.to_datetime(log_data['Date'])
log_data['Time'] = pd.to_datetime(log_data['Time'], format='%H:%M:%S')

# Extract numerical features from 'Date' and 'Time' columns
log_data['Year'] = log_data['Date'].dt.year
log_data['Month'] = log_data['Date'].dt.month
log_data['Day'] = log_data['Date'].dt.day
log_data['Hour'] = log_data['Time'].dt.hour

# Drop the original 'Date' and 'Time' columns
log_data.drop(['Date', 'Time'], axis=1, inplace=True)

# Save the preprocessed data to a new CSV file
log_data.to_csv('preprocessed_web_logs_for_prediction.csv', index=False)

# Load Data
log_data = pd.read_csv('preprocessed_web_logs_for_prediction.csv')

# Traffic Forecasting
traffic_features = ['Year', 'Month', 'Day', 'Hour']  
log_data['Timestamp'] = pd.to_datetime(log_data['Timestamp'])
log_data['Number of Requests'] = log_data.groupby(pd.Grouper(key='Timestamp', freq='h'))['Timestamp'].transform('count')
traffic_target = 'Number of Requests'  
X_traffic = log_data[traffic_features]
y_traffic = log_data[traffic_target]
X_train_traffic, X_test_traffic, y_train_traffic, y_test_traffic = train_test_split(X_traffic, y_traffic, test_size=0.2, random_state=42)
traffic_model = RandomForestRegressor()  
traffic_model.fit(X_train_traffic, y_train_traffic)
y_pred_traffic = traffic_model.predict(X_test_traffic)
mse_traffic = mean_squared_error(y_test_traffic, y_pred_traffic)
print(f'Traffic Forecasting Mean Squared Error: {mse_traffic}')

# Error Prediction
def predict_error(logs):
    # Preprocess data
    logs['Timestamp'] = pd.to_datetime(logs['Timestamp'], errors='coerce')
    logs['Year'] = logs['Timestamp'].dt.year
    logs['Month'] = logs['Timestamp'].dt.month
    logs['Day'] = logs['Timestamp'].dt.day
    logs['Hour'] = logs['Timestamp'].dt.hour
    X_error = logs[['Year', 'Month', 'Day', 'Hour', 'Status Code']]
    y_error = logs['Status Code'].apply(lambda x: 1 if x != 200 else 0)

    # Drop rows with unexpected 'Timestamp' values
    logs = logs[logs['Timestamp'].notna()]

    # Split data into train and test sets
    X_train_error, X_test_error, y_train_error, y_test_error = train_test_split(X_error, y_error, test_size=0.2, random_state=42)
    error_model = RandomForestClassifier()
    error_model.fit(X_train_error, y_train_error)

    # Predict
    y_pred_error = error_model.predict(X_test_error)
    accuracy_error = accuracy_score(y_test_error, y_pred_error)
    print(f'Error Prediction Accuracy: {accuracy_error}')

    # Return the prediction accuracy and data for visualization
    return accuracy_error, y_test_error, y_pred_error

# Status Code Prediction
def predict_status_code(logs):
    # Preprocess data
    logs['Timestamp'] = pd.to_datetime(logs['Timestamp'], errors='coerce')
    logs['Year'] = logs['Timestamp'].dt.year
    logs['Month'] = logs['Timestamp'].dt.month
    logs['Day'] = logs['Timestamp'].dt.day
    logs['Hour'] = logs['Timestamp'].dt.hour
    X_status_code = logs[['Year', 'Month', 'Day', 'Hour', 'Endpoint']]
    y_status_code = logs['Status Code']

    # Handle categorical data if 'Endpoint' is a categorical variable
    X_status_code = pd.get_dummies(X_status_code, columns=['Endpoint'])

    # Split data into train and test sets
    X_train_status_code, X_test_status_code, y_train_status_code, y_test_status_code = train_test_split(X_status_code, y_status_code, test_size=0.2, random_state=42)

    # Train model
    status_code_model = RandomForestClassifier()
    status_code_model.fit(X_train_status_code, y_train_status_code)

    # Predict
    y_pred_status_code = status_code_model.predict(X_test_status_code)

    # Evaluate
    accuracy_status_code = accuracy_score(y_test_status_code, y_pred_status_code)
    print(f'Status Code Prediction Accuracy: {accuracy_status_code}')

    # Return the prediction accuracy and data for visualization
    return accuracy_status_code, y_test_status_code, y_pred_status_code


# Page Popularity Prediction
def predict_page_popularity(logs):
    # Convert 'Timestamp' to datetime and extract features
    logs['Timestamp'] = pd.to_datetime(logs['Timestamp'])
    logs['Year'] = logs['Timestamp'].dt.year
    logs['Month'] = logs['Timestamp'].dt.month
    logs['Day'] = logs['Timestamp'].dt.day
    logs['Hour'] = logs['Timestamp'].dt.hour
    logs['Weekday'] = logs['Timestamp'].dt.weekday

    # Group by 'Page' and 'Timestamp' to get the count of requests
    page_popularity = logs.groupby(['Page', 'Year', 'Month', 'Day', 'Hour', 'Weekday']).size().reset_index(name='Number of Requests')

    # Prepare features and target
    X_page = page_popularity[['Page', 'Year', 'Month', 'Day', 'Hour', 'Weekday']]  # Include 'Page' in the features
    y_page = page_popularity['Number of Requests']

    # One-hot encode the 'Page' feature if it's categorical
    X_page = pd.get_dummies(X_page, columns=['Page'])

    # Split the data into training and testing sets
    X_train_page, X_test_page, y_train_page, y_test_page = train_test_split(X_page, y_page, test_size=0.2, random_state=42)

    # Initialize and train the model
    page_model = RandomForestRegressor(n_estimators=100, random_state=42)
    page_model.fit(X_train_page, y_train_page)

    # Make predictions
    y_pred_page = page_model.predict(X_test_page)

    # Evaluate the model
    mse_page = mean_squared_error(y_test_page, y_pred_page)
    print(f'Page Popularity Prediction Mean Squared Error: {mse_page}')

    # Return the mean squared error and data for visualization
    return mse_page, y_test_page, y_pred_page

def predict_load(log_data):
    # Convert 'Request Method' to a categorical variable
    log_data['Method_Cat'] = log_data['Request Method'].astype('category').cat.codes

    # Extract hour from 'Timestamp' and create a new feature
    log_data['Hour'] = pd.to_datetime(log_data['Timestamp']).dt.hour

    # Prepare the features and target variable
    X_load = log_data[['Hour', 'Method_Cat']]  # Features
    y_load = log_data['Page']  # Target variable

    # Split the data into training and testing sets
    X_train_load, X_test_load, y_train_load, y_test_load = train_test_split(X_load, y_load, test_size=0.2, random_state=42)

    # Initialize the Gradient Boosting Classifier
    load_model = GradientBoostingClassifier(n_estimators=100, random_state=42)

    # Train the model
    load_model.fit(X_train_load, y_train_load)

    # Predict user behavior
    load_predictions = load_model.predict(X_test_load)

    # Evaluate the model
    load_model_accuracy = accuracy_score(y_test_load, load_predictions)

    # Return the model accuracy and predictions
    return load_model_accuracy, y_test_load, load_predictions

#user behavior

# Convert 'Status Code' to a binary variable where 1 indicates a server error (500)
log_data['Is_Error'] = (log_data['Status Code'] == 500).astype(int)

# Prepare the features and target variable
X = log_data[['Hour']]  # Feature
y = log_data['Is_Error']  # Target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict server load issues
predictions = model.predict(X_test)


# Predict user behavior on the test set
behavior_predictions = model.predict(X_test)

# Calculate the accuracy of the model
behavior_model_accuracy = accuracy_score(y_test, behavior_predictions)
print(f'User Behavior Prediction Model Accuracy: {behavior_model_accuracy:.2f}')

def visualize_prediction_models(y_test, predictions, model_name):
    """
    Visualizes the prediction models using various visualizations.

    Args:
    - y_test (array-like): Array of true labels.
    - predictions (array-like): Array of predicted labels.
    - model_name (str): Name of the prediction model.

    Returns:
    - List of tuples containing the figure and title for each visualization.
    """
    visualizations = []

    if model_name == 'Error Prediction':
        # Error Prediction Visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(confusion_matrix(y_test, predictions), annot=True, fmt='d', cmap='Blues', cbar_kws={'label': 'Number of Predictions'}, ax=ax)
        ax.set_xlabel('Predicted')
        ax.set_ylabel('Actual')
        ax.set_title('Error Prediction Confusion Matrix')
        visualizations.append((fig, 'Error Prediction Confusion Matrix'))

    elif model_name == 'Status Code Prediction':
        # Status Code Prediction Visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(confusion_matrix(y_test, predictions), annot=True, fmt='d', cmap='Blues', cbar_kws={'label': 'Number of Predictions'}, ax=ax)
        ax.set_xlabel('Predicted')
        ax.set_ylabel('Actual')
        ax.set_title('Status Code Prediction Confusion Matrix')
        visualizations.append((fig, 'Status Code Prediction Confusion Matrix'))

    elif model_name == 'Page Popularity Prediction':
        # Page Popularity Prediction Visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(y_test, predictions, alpha=0.5, label='Data points')
        ax.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', label='Ideal fit line')
        ax.set_xlabel('Actual Page Requests')
        ax.set_ylabel('Predicted Page Requests')
        ax.set_title('Page Popularity Prediction: Actual vs Predicted')
        ax.legend()
        visualizations.append((fig, 'Page Popularity Prediction: Actual vs Predicted'))

    elif model_name == 'Load Prediction':
        # Load Prediction Visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(confusion_matrix(y_test, predictions), annot=True, fmt='d', cmap='Blues', cbar_kws={'label': 'Number of Predictions'}, ax=ax)
        ax.set_xlabel('Predicted')
        ax.set_ylabel('Actual')
        ax.set_title('Load Prediction Confusion Matrix')
        visualizations.append((fig, 'Load Prediction Confusion Matrix'))

    elif model_name == 'User Behavior Prediction':
        # User Behavior Prediction Visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(confusion_matrix(y_test, predictions), annot=True, fmt='d', cmap='Blues', cbar_kws={'label': 'Number of Predictions'}, ax=ax)
        ax.set_xlabel('Predicted')
        ax.set_ylabel('Actual')
        ax.set_title('User Behavior Prediction Confusion Matrix')
        visualizations.append((fig, 'User Behavior Prediction Confusion Matrix'))

    else:
        print("Invalid model name. Please provide one of the following: 'Error Prediction', 'Status Code Prediction', 'Page Popularity Prediction', 'Load Prediction', 'User Behavior Prediction'.")

    return visualizations
