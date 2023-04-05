# get the location of the cities
from typing import List
from sklearn.metrics import classification_report, f1_score, accuracy_score, recall_score, precision_score, confusion_matrix

def get_location(city: List[str])->List[str]:
    """function to get the location of the cities

    Args:
        city (list): list of cities

    Returns:
        _type_:  list of locations
    """    
    geolocator = Nominatim(user_agent='myapp')
    loc_nationals = city
    region = []
    for city in loc_nationals:
        location = geolocator.geocode(city)
        if location:
            country = location.raw["display_name"].split(',')[2]
            region.append(country)
        else:
            region.append('Not Found')
    return region

def get_location_comprehesion(cities: List[str]) -> List[str]:
    geolocator = Nominatim(user_agent="myapp")
    return [
        geolocator.geocode(city).raw["display_name"].split(",")[2]
        if geolocator.geocode(city)
        else "Not Found"
        for city in cities
        ]



def optimize_threshold(df, score_col, y_true):
    """Function to optimize the threshold for a binary classification problem

    Args:
        df (_type_): DataFrame with the scores and the true labels
        score_col (_type_): Column with the scores
        y_true (_type_): True values

    Returns:
        _type_: DataFrame with the metrics for each threshold
    """    
    low, high = df[score_col].agg([min ,max])
    grid = np.linspace(low, high, 1000)
    metrics = {}
    for i, umbral in tqdm(enumerate(grid)):
        y_pred = df[score_col].ge(umbral).astype(int)
        metrics[i] = {
            "Accuracy": accuracy_score(y_true, y_pred),
            "F1": f1_score(y_true, y_pred),
            "Recall": recall_score(y_true, y_pred),
            "Precision": precision_score(y_true, y_pred)
                    }
    results = pd.DataFrame.from_dict(metrics, orient = "index")
    results.set_index(grid,inplace = True)
    return results