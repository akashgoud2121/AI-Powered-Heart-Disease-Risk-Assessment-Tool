def load_model(model_path):
    import joblib
    return joblib.load(model_path)

def predict(model, input_data):
    return model.predict(input_data)