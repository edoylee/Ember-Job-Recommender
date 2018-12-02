import pandas as pd
import numpy as np
from scipy import spatial
from sklearn.feature_extraction.text import TfidfVectorizer
from selenium.webdriver import Firefox
import time
import random

CUSTOM_STOP = [
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep",
    "oct", "nov", "dec"]


class LinkedinScraper():
    
    def __init__(self, param=None):
        self.browser = Firefox()
        self.browser.get('https://www.linkedin.com')
    
    def sleep(start=5, end=15):
        return time.sleep(random.randint(5, 15))
    
    def find_profile(self, name):
        search_bar = self.browser.find_element_by_css_selector('#ember41 > input:nth-child(1)')
        search_bar.click()
        self.sleep()
        search_bar.send_keys(name)
        search_button = self.browser.find_element_by_css_selector(
            '.search-typeahead-v2__button > span:nth-child(1) > li-icon:nth-child(2) > svg:nth-child(1)'
        )
        search_button.click()
        self.sleep()
        search_results = self.browser.find_elements_by_class_name('name')
        search_results[0].click()
        
    def scroll(self):
        sections = self.browser.find_elements_by_class_name('pv-profile-section')
        for section in sections:
            section.location_once_scrolled_into_view
            self.sleep()
        
    def expand_page(self):
        rec = self.browser.find_elements_by_class_name('pv-profile-section__see-more-inline')
        rec[1].location_once_scrolled_into_view
        rec[1].click()
        self.sleep()
        summary_section = self.browser.find_element_by_class_name('pv-top-card-section__summary')
        summary_section.location_once_scrolled_into_view
        showmores = self.browser.find_elements_by_class_name('pv-profile-section__card-action-bar')
        showmores[0].click()
        self.sleep()
        skills_section = self.browser.find_element_by_class_name('pv-skill-categories-section')
        skills_section.location_once_scrolled_into_view
        showmores[1].click()
        self.sleep()
        experience_section = self.browser.find_element_by_class_name('experience-section')
        experience_section.location_once_scrolled_into_view
        experience_seemores = self.browser.find_elements_by_link_text('See more')
        for seemore in experience_seemores:
            seemore.click()
            sleep()
    
    def scrape_page(self):
        summary = []
        find_summary = self.browser.find_element_by_class_name('pv-top-card-section__summary-text')
        summary.append(find_summary.text)
        experience = []
        find_experience = self.browser.find_element_by_id('oc-background-section')
        experience.append(find_experience.text)
        skills = []
        find_skills = self.browser.find_element_by_class_name('pv-skill-categories-section')
        skills.append(find_skills.text)
        recommendations = []
        find_recommendations = self.browser.find_element_by_class_name('pv-recommendations-section')
        recommendations.append(find_recommendations.text)
        profile_df = pd.DataFrame({'summary': summary,
                                   'experience': experience, 
                                   'skills': skills, 
                                   'recommendations': recommendations})
        return profile_df
    
    def concat_strings(self, word_list):
        total_cleaned = ''
        for word in word_list:
            total_cleaned += (word + ' ')
        return total_cleaned
    
    def get_consolidated_profile(self, columns):
        total_string = ''
        for column in columns:
            total_string += concat_strings(chris_profile_df[column])
        return [total_string]
    
    def transform(self, name):
        self.find_profile(name)
        self.scroll()
        self.expand_page()
        profile_df = self.scrape_page()
        consolidated_df = self.get_consolidated_profile(profile_df)
        final_df = pd.DataFrame({'profile': consolidated_df})
        return final_df

class ScrapeGlass():
    """ ScrapeGlass is used to scrape job postings from Glassdoor.
    
    Basic Process:
    
    • The search method will go to the url and search for the query.
    
    • The click_wait method will click the second job posting to
      trigger the automatic pop-up window, then it will find the 
      x-button in the corner and click it.
      
    • The loop_pages method will find the number of pages at the 
      bottom of the screen use that number in a for loop to iterate 
      through all of the pages for the given query.
      
    • The get_job_postings method is called in the loop_pages function
      in order to iterate through every job listing on the page and scrape
      the descriptions. The descriptions are then appended to a class variable.
      
    • Finally the return_job_descriptions method is called to prompt the user
      to decide whether or not to save the scraped results to a csv file.
    
    All of this is being done through the transform method.
    
    example:
    
        url = 'www.glassdoor.com'
        query = 'Data Scientist'
    
        test = ScrapeGlass()
        jobs = test.transform(url, query)
    
    Final Notes:
    
        If the program is interupted for any reason the user will still be prompted
        on whether or not to proceed with exporting to csv. 
    
    """
    
    def __init__(self, param=None):
        self.browser = Firefox()
        self.job_descriptions = []
    
    def click_wait(self):
        """ This method triggers the automatic pop-up window and exits out of it."""
        
        listings = self.browser.find_elements_by_class_name('jl')
        listings[1].click()
        x_button = self.browser.find_element_by_class_name('xBtn')
        x_button.click()
    
    def return_job_descriptions(self):
        """ This method prompts the user whether or not to convert to csv"""
        
        print(len(self.job_descriptions))
        check_variable = input('\nProceed? (yes / no) ')
        if check_variable == 'yes':
            name = input('Enter name of data')
            self.convert_to_csv(self.job_descriptions, ('../data/%s.csv' % name))
        else:
            return self.job_descriptions
    
    def sleep(start=5, end=15):
        return time.sleep(random.randint(5, 15))
        
    def search(self, url, query):
        """ This method goes to the url, and searchs for the query"""
        
        self.browser.get(url)
        self.sleep()
        keyword_search = self.browser.find_element_by_css_selector('#KeywordSearch')
        keyword_search.click()
        keyword_search.send_keys(query)
        start_search = self.browser.find_element_by_css_selector('#HeroSearchButton')
        start_search.click()
    
    def loop_pages(self):
        """ This method iterates through all available pages"""
        
        pages = self.browser.find_elements_by_class_name('page')
        while len(pages) == 5:
            self.get_job_postings()
            next_button = self.browser.find_element_by_class_name('next')
            next_button.click()
            self.sleep()
        return self.return_job_descriptions()
    
    def get_job_postings(self):
        """ This method iterates through all of the listings and appends 
        them to the class variable self.job_descriptions"""
        
        job_listings = self.browser.find_elements_by_class_name('jl')
        self.sleep()
        for job in job_listings:
            job.location_once_scrolled_into_view
            job.click()
            self.sleep()
            content = self.browser.find_element_by_class_name('jobDescriptionContent')
            self.job_descriptions.append(content.text)
            choice = random.randint(1,3)
            if choice == 2:
                tabs = self.browser.find_elements_by_class_name('tabLabel')
                try:    
                    tabs[random.randint(1,2)].click()
                except IndexError:
                    pass
            self.sleep()
        return self.job_descriptions
    
    def convert_to_csv(self, final_content, name):
        """ This method converts the list final_content into a pandas 
        dataframe and adds a 'lables' column of zeros"""
        
        final_txdf = pd.DataFrame({'jobs': final_content})
        final_txdf['labels'] = np.zeros(final_txdf.shape[0])
        final_txdf.to_csv(name)
    
    def transform(self, url, query):
        """ This method takes the url, and query as inputs and outputs either
        an exported csv file or a list of jobs"""
        self.search(url, query)
        self.click_wait()
        try:
            self.loop_pages()
        except:
            return self.return_job_descriptions()
        self.return_job_descriptions()

class PreprocessData():
    
    def __init__(self, param=None):
        self.param = param
        self.vectorizer = TfidfVectorizer(stop_words=CUSTOM_STOP)
        
    
    def bring_in_data(self, X, y):
        df = pd.read_csv(X, index_col=0)
        df = df.dropna()
        y_vector = pd.read_csv(y, index_col=0)
        full_df = y_vector['profile'].append(df['jobs'])
        return full_df
    
    def get_tfidf(self, df):
        self.vectorizer.fit(df)
        transformed_model = self.vectorizer.transform(df)
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
    
    def transform(self, X, y):
        full_df = self.bring_in_data(X, y)
        tfidf_df = self.get_tfidf(full_df)
        sorted_distances, indices = self.get_distances(tfidf_df)
        total_df = self.get_total_df(indices, full_df, sorted_distances, tfidf_df)
        return total_df

class Predict():
    
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


if __name__ == '__main__':
    pass

