import pandas as pd

class ConvertData():
    def __init__(self, param=None):
        self.param = param
        
    def preprocess_data(self, data):
        df = pd.read_csv(data, index_col=0)
        split_jobs = [job.split('\n') for job in df.jobs]
        text_df = pd.DataFrame({'jobs': split_jobs, 'labels': df.labels})
        return text_df
    
class TrainX():
    def __init__(self, df):
        self.filled_df = df.copy()
    
    def assign_labels(self):
        for i in range(self.filled_df.shape[0]):
            for chunk in self.filled_df.iloc[i,0]:
                print(chunk)
            label = input('\nyes / no (quit) ')
            print('\n\n', '-'*100, '\n')
            if label == 'yes':
                self.filled_df.iat[i,1] = 1.0
            elif label == 'no':
                self.filled_df.iat[i,1] = -1.0
            elif label == 'quit':
                return self.convert_to_string(self.filled_df)
        return self.convert_to_string(self.filled_df)
    
    def convert_to_string(self, df):
        for i in range(df.shape[0]):
            total_string = ''
            for chunk in df.iloc[i,0]:
                total_string += chunk
                df.iat[i,0] = total_string
        return df
    
    def transform(self):
        try:
            final_df = self.assign_labels()
        except:
            return self.convert_to_string(self.filled_df)
        return self.convert_to_string(final_df)