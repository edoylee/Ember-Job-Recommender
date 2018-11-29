import pandas as pd
import numpy as np
from scipy import spatial
from sklearn.feature_extraction.text import TfidfVectorizer

class preprocess_data():
    def __init__(self, param=None):
        self.param = param
    
    def bring_in_data(self, X, y):
        df = pd.read_csv(X, index_col=0)
        df = df.dropna()
        y_vector = pd.read_csv(y, index_col=0)
        full_df = y_vector['profile'].append(df['jobs'])
        return full_df
    
    def get_tfidf(self, df, vectorizer):
        vectorizer.fit(df)
        transformed_model = vectorizer.transform(df)
        tfidf_df = pd.DataFrame(transformed_model.toarray())
        return tfidf_df
    
    def get_distances(self, df):
        profile = df.iloc[0, :]
        distances = []
        for i in range(len(df.index)):
            distances.append(spatial.distance.cosine(profile, df.iloc[i,:]))
        sorted_distances = np.sort(distances)
        indices = np.argsort(distances)
        return sorted_distances, indices
    
    def get_total_df(self, indices, full_df, sorted_distances, tfidf_df):
        indices_df = pd.DataFrame({'indices': indices})
        sorted_distances_df = pd.DataFrame({'distances': sorted_distances})
        sorted_df = pd.DataFrame({'jobs': full_df.iloc[indices]}).set_index(np.arange(0,120))
        sorted_df['labels'] = np.zeros(120)
        sorted_tfidf = pd.DataFrame(tfidf_df.iloc[indices]).set_index(np.arange(0,120))
        total_df = pd.concat([indices_df, sorted_df, sorted_distances_df, sorted_tfidf], axis=1)
        total_df.iat[0,2] = 10.0
        return total_df
    
    def transform(self, X, y, vectorizer):
        full_df = self.bring_in_data(X, y)
        tfidf_df = self.get_tfidf(full_df, vectorizer)
        sorted_distances, indices = self.get_distances(tfidf_df)
        total_df = self.get_total_df(indices, full_df, sorted_distances, tfidf_df)
        return total_df

class yes():
    def __init__(self, df):
        self.df = df
    
    def prompt_user(self, df, index):
        recommended_posting = pd.DataFrame(df.iloc[index, :]).T
        original_index = int(recommended_posting['indices'])
        label_index = self.df[self.df['indices'] == original_index].index[0]
        print(recommended_posting.iloc[0,1])
        label = input("\nyes/no (quit)")
        if label == 'quit':
            return "Done"
        if label == 'yes':
            self.df.iat[label_index,2] = 1.0
        if label == 'no':
            self.df.iat[label_index,2] = -1.0
        return self.df
    
    def improve_yes(self, df):
        yes_df = pd.DataFrame(df[df['labels'] == 1.0])
        yes_remains = pd.DataFrame(df[df['labels'] == 0.0])
        yes_remains = yes_remains.set_index(np.arange(0, yes_remains.shape[0]))
        distances_from_yes = np.zeros((yes_remains.shape[0], yes_df.shape[0]))
        for i in range(yes_df.shape[0]):
            for j in range(yes_remains.shape[0]):
                distances_from_yes[j,i] = (spatial.distance.cosine(yes_df.iloc[0,4:], yes_remains.iloc[j,4:]))
        yes_remains['distances_from_yes'] = np.sum(distances_from_yes, axis=1)
        return yes_remains
    
    def improve_no(self, df):
        no_df = pd.DataFrame(df[df['labels'] == -1.0])
        no_remains = pd.DataFrame(df[df['labels'] == 0.0])
        no_remains = no_remains.set_index(np.arange(0, no_remains.shape[0]))
        distances_from_no = np.zeros((no_remains.shape[0], no_df.shape[0]))
        for i in range(no_df.shape[0]):
            for j in range(no_remains.shape[0]):
                distances_from_no[j,i] = (spatial.distance.cosine(no_df.iloc[0,4:], no_remains.iloc[j,4:]))
        no_remains['distances_from_no'] = np.sum(distances_from_no, axis=1)
        return no_remains
    
    def find_next_best(self, df, index=1):
        adjusted_df = self.prompt_user(df, index)
        try:
            yes_remains = self.improve_yes(adjusted_df)
            no_remains = self.improve_no(adjusted_df)
        except TypeError:
            return self.df
        total_distance = yes_remains.distances + yes_remains.distances_from_yes - no_remains.distances_from_no
        remains = yes_remains.copy()
        remains['total_distance'] = total_distance
        next_best_index = remains.total_distance.idxmin()
        return self.find_next_best(remains, next_best_index)
    