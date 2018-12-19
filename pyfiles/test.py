from predictNew import LinkedinScraper, PreprocessData, Predict
import pandas as pd

data = PreprocessData()
total_df = data.transform('data/dsjobs_training_culled.csv', 'data/ethan_profile.csv')
prediction = Predict(total_df)
index = 1
recommended_posting = pd.DataFrame(total_df.iloc[index, :]).T

def handle_yes():
    global index
    global total_df
    original_index = int(recommended_posting['indices'])
    label_index = total_df[total_df['indices'] == original_index].index[0]
    total_df.iat[label_index,2] = 1.0
    remains, next_best_index = find_next_best()
    index = next_best_index
    job_desc = remains.iloc[next_best_index, 1]
    
def find_next_best():
    try:
        yes_remains = prediction.improve_yes(total_df)
        no_remains = prediction.improve_no(total_df)
    except TypeError:
        return prediction.convert_to_csv()
    total_distance = yes_remains.distances + yes_remains.distances_from_yes - no_remains.distances_from_no
    remains = yes_remains.copy()
    remains['total_distance'] = total_distance
    next_best_index = remains.total_distance.idxmin()
    return remains, next_best_index
