import pandas as pd # pyright: ignore[reportMissingModuleSource]
from sklearn.model_selection import train_test_split # pyright: ignore[reportMissingModuleSource]
from sklearn.ensemble import RandomForestRegressor # pyright: ignore[reportMissingModuleSource]
from sklearn.preprocessing import LabelEncoder # type: ignore
import joblib # pyright: ignore[reportMissingImports]

try:

    print("Loading dataset...")

    df = pd.read_csv("dataset.csv")

    print("Dataset loaded")
    print(df.head())

    # remove missing values
    df = df.dropna()

    # convert category to number
    encoder = LabelEncoder()
    df["Product_Category"] = encoder.fit_transform(df["Product_Category"])

    # features and label
    X = df.drop("Price", axis=1)
    y = df["Price"]

    print("Training model...")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor()

    model.fit(X_train, y_train)

    joblib.dump(model, "pricing_model.pkl")

    print("Model trained successfully")

except Exception as e:

    print("Error occurred:")
    print(e)