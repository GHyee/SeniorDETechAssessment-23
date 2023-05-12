# import the necessary libraries
import pandas as pd
import h2o
from h2o.automl import H2OAutoML

# Load dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/car/car.data"
data = pd.read_csv(url, names=["buying", "maint", "doors", "persons", "lug_boot", "safety", "class"])

# specify the predictor and response variables
predictors = ["maint", "doors", "lug_boot", "safety", "class"]
response = "buying"
df = data[predictors]

# initialize the H2O cluster
h2o.init()

# convert the pandas dataframe to an H2O frame
h2o_df = h2o.H2OFrame(df)

# split the data into training and test sets
train, test = h2o_df.split_frame(ratios=[0.7])

# initialize the H2O AutoML object
automl = H2OAutoML(max_models=10, seed=1)

# train the model
automl.train(x=predictors, y=response, training_frame=train)

# view the leaderboard
print(automl.leaderboard)

# make predictions on the test set
predictions = automl.leader.predict(test)


def make_prediction(AutoML, data, col_names):
    """
    Makes a prediction using the best H2O AutoML model.
    
    Args:
    - AutoML: an H2OAutoML object that contains the best model.
    - data: a list of values to use as input for the prediction.
    
    Returns:
    - The predicted value.
    """
    
    # Convert data to a 2D H2OFrame
    df = pd.DataFrame(data, columns=col_names)
    h2o_data = h2o.H2OFrame(df)
    
    # Make the prediction
    prediction = AutoML.predict(h2o_data)
    
    # Convert the prediction to a Python object
    prediction = prediction[0, 0]
    
    return prediction


prediction = make_prediction(automl, ["high", 4, "big", "high", "good"], predictors)
print(prediction)
