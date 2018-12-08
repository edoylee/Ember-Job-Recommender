import pandas as pd
import numpy as np
from scipy import spatial
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from selenium.webdriver import Firefox
import time
import random
import getpass
from flask import Flask, render_template
app = Flask(__name__, static_url_path="")


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
    "oct", "nov", "dec", "endorse", "endorsement", "endorsements"]


class LinkedinScraper():
    """ The LinkedinScraper will scrape the linkedin profile of the given name.

    Basic Process:

        • The find_profile method is used to navigate to the given profile

        • The expand_page method is used to find summary, experience, skills, and recommendations
        sections and expand them to be scrapable

        • The scrape_page method is used to scrape the same four sections if they exist and return
        empty strings otherwise

        • The get_consolidated_profile method will take a dataframe of 4 columns and concatenate them
        into one string to be ready for nlp.

    example:

        test = LinkedinScraper()
        final_df = test.transform('NAME')
        """
    def __init__(self, param=None):
        self.browser = Firefox()
        self.browser.get('https://www.linkedin.com')

    def sleep(self, start=5, end=15):
        return time.sleep(random.randint(start, end))

    def go_to_profile(self):
        email = input('Please Enter Email ')
        password = getpass.getpass('Please Enter Password ')
        login_email = self.browser.find_element_by_class_name('login-email')
        login_email.click()
        login_email.send_keys(email)
        self.sleep(start=2, end=5)
        login_password = self.browser.find_element_by_class_name('login-password')
        login_password.click()
        login_password.send_keys(password)
        submit_button = self.browser.find_element_by_class_name('submit-button')
        submit_button.click()
        self.sleep(start=2, end=5)
        profile_button = self.browser.find_element_by_class_name('tap-target')
        profile_button.click()
        self.sleep()

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
        try:
            rec = self.browser.find_elements_by_class_name('pv-profile-section__see-more-inline')
            rec[1].location_once_scrolled_into_view
            rec[1].click()
        except:
            pass
        self.sleep()
        try:
            summary_section = self.browser.find_element_by_class_name('pv-top-card-section__summary')
            summary_section.location_once_scrolled_into_view
            showmores = self.browser.find_elements_by_class_name('pv-profile-section__card-action-bar')
            showmores[0].click()
        except:
            pass
        self.sleep()
        try:
            skills_section = self.browser.find_element_by_class_name('pv-skill-categories-section')
            skills_section.location_once_scrolled_into_view
            showmores[1].click()
        except:
            pass
        self.sleep()
        try:
            experience_section = self.browser.find_element_by_class_name('experience-section')
            experience_section.location_once_scrolled_into_view
            experience_seemores = self.browser.find_elements_by_link_text('See more')
            for seemore in experience_seemores:
                seemore.click()
                sleep()
        except:
            pass

    def second_expand_page(self):
        summary_section = self.browser.find_element_by_class_name('pv-top-card-section__summary')
        summary_section.location_once_scrolled_into_view
        try:
            showmores = self.browser.find_elements_by_class_name('pv-profile-section__card-action-bar')
            showmores[0].click()
        except:
            pass
        self.sleep()
        experience_section = self.browser.find_element_by_class_name('experience-section')
        experience_section.location_once_scrolled_into_view
        experience_listings = self.browser.find_elements_by_class_name('pv-profile-section__list-item')
        self.sleep()
        for listing in experience_listings:
            listing.location_once_scrolled_into_view
            self.sleep()
        experience_seemores = self.browser.find_elements_by_link_text('See more')
        self.sleep()
        for seemore in experience_seemores:
            seemore.click()
            self.sleep()
        skills_section = self.browser.find_element_by_class_name('pv-skill-categories-section')
        skills_section.location_once_scrolled_into_view
        self.sleep()
        try:
            showmores = self.browser.find_elements_by_class_name('pv-profile-section__card-action-bar')
            showmores[1].click()
        except IndexError:
            showmores[0].click()
        try:
            self.sleep()
            rec = self.browser.find_elements_by_class_name('pv-profile-section__see-more-inline')
            rec[1].click()
        except:
            pass

    def scrape_page(self):
        summary = []
        try:
            find_summary = self.browser.find_element_by_class_name('pv-top-card-section__summary-text')
            summary.append(find_summary.text)
        except:
            summary.append('')
        experience = []
        try:
            find_experience = self.browser.find_element_by_id('oc-background-section')
            experience.append(find_experience.text)
        except:
            experience.append('')
        education = []
        try:
            self.sleep()
            find_education = self.browser.find_element_by_class_name('education-section')
            find_education.append(education.text)
        except:
            education.append('')
        skills = []
        try:
            find_skills = self.browser.find_element_by_class_name('pv-skill-categories-section')
            skills.append(find_skills.text)
        except:
            skills.append('')
        recommendations = []
        try:
            find_recommendations = self.browser.find_element_by_class_name('pv-recommendations-section')
            recommendations.append(find_recommendations.text)
        except:
            recommendations.append('')
        profile_df = pd.DataFrame({'summary': summary,
                                   'experience': experience,
                                   'education': education,
                                   'skills': skills,
                                   'recommendations': recommendations})
        return profile_df

    def concat_strings(self, word_list):
        total_cleaned = ''
        for word in word_list:
            total_cleaned += (word + ' ')
        return total_cleaned

    def get_consolidated_profile(self, df, columns):
        total_string = ''
        for column in columns:
            total_string += self.concat_strings(df[column])
        return [total_string]

    def convert_to_csv(self, df):
        check_variable = input('Proceed? (yes / no)')
        if check_variable == 'yes':
            name = input('Enter name: ')
            df.to_csv('~/galvanize/capstone/Ember-Job-Recommender/data/%s.csv' % name)
        else:
            return df

    def transform(self):
        self.go_to_profile()
        self.second_expand_page()
        profile_df = self.scrape_page()
        consolidated_df = self.get_consolidated_profile(profile_df, profile_df.columns)
        titles = ''
        companies = ''
        final_df = pd.DataFrame({'titles': titles,
                                    'companies': companies,
                                    'jobs': consolidated_df})
        return self.convert_to_csv(final_df)

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
        self.titles = []
        self.companies = []
        self.job_descriptions = []

    def click_wait(self):
        """ This method triggers the automatic pop-up window and exits out of it."""

        listings = self.browser.find_elements_by_class_name('jl')
        listings[1].click()
        x_button = self.browser.find_element_by_class_name('xBtn')
        x_button.click()

    def return_job_descriptions(self):
        """ This method prompts the user whether or not to convert to csv"""

        print(len(self.titles), len(self.companies), len(self.job_descriptions))
        check_variable = input('\nProceed? (yes / no) ')
        if check_variable == 'yes':
            name = input('Enter name of data')
            self.convert_to_csv(self.titles,
                                self.companies,
                                self.job_descriptions,
                                ('~/galvanize/capstone/Ember-Job-Recommender/data/%s.csv' % name))
        else:
            return self.job_descriptions

    def sleep(self, start=5, end=15):
        return time.sleep(random.randint(5, 15))

    def search(self, query):
        """ This method goes to the url, and searchs for the query"""

        self.browser.get('https://www.glassdoor.com')
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
            title = self.browser.find_element_by_class_name('header')
            self.titles.append(title.text)
            company = self.browser.find_element_by_class_name('compInfo')
            self.companies.append(company.text)
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

    def convert_to_csv(self, titles, companies, final_content, name):
        """ This method converts the list final_content into a pandas
        dataframe and adds a 'lables' column of zeros"""

        final_txdf = pd.DataFrame({'titles': titles,
                                    'companies': companies,
                                    'jobs': final_content})
        final_txdf.to_csv(name)

    def transform(self, query):
        """ This method takes the url, and query as inputs and outputs either
        an exported csv file or a list of jobs"""
        self.search(query)
        self.click_wait()
        try:
            self.loop_pages()
        except:
            return self.return_job_descriptions()
        self.return_job_descriptions()

class ScrapeGlassHot():
    """ ScrapeGlassHot is used to scrape new job postings from Glassdoor in
    that are labeled as 'hot', or 'new', to be used for test data.

    """

    def __init__(self, param=None):
        self.browser = Firefox()
        self.titles = []
        self.companies = []
        self.job_descriptions = []

    def click_wait(self):
        """ This method triggers the automatic pop-up window and exits out of it."""

        listings = self.browser.find_elements_by_class_name('jl')
        listings[1].click()
        x_button = self.browser.find_element_by_class_name('xBtn')
        x_button.click()

    def return_job_descriptions(self):
        """ This method prompts the user whether or not to convert to csv"""

        print(len(self.titles), len(self.companies), len(self.job_descriptions))
        check_variable = input('\nProceed? (yes / no) ')
        if check_variable == 'yes':
            name = input('Enter name of data')
            self.convert_to_csv(self.titles,
                                self.companies,
                                self.job_descriptions,
                                ('~/galvanize/capstone/Ember-Job-Recommender/data/%s.csv' % name))
        else:
            return self.job_descriptions

    def sleep(self, start=5, end=15):
        return time.sleep(random.randint(5, 15))

    def search(self, query):
        """ This method goes to the url, and searchs for the query"""

        self.browser.get('https://www.glassdoor.com')
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

        hot_listings = self.browser.find_elements_by_class_name('hotListing')
        self.sleep()
        for hot in hot_listings:
            hot.location_once_scrolled_into_view
            hot.click()
            self.sleep()
            title = self.browser.find_element_by_class_name('header')
            self.titles.append(title.text)
            company = self.browser.find_element_by_class_name('compInfo')
            self.companies.append(company.text)
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

    def convert_to_csv(self, titles, companies, final_content, name):
        """ This method converts the list final_content into a pandas
        dataframe and adds a 'lables' column of zeros"""

        final_txdf = pd.DataFrame({'titles': titles,
                                    'companies': companies,
                                    'jobs': final_content})
        final_txdf.to_csv(name)

    def transform(self, query):
        """ This method takes the url, and query as inputs and outputs either
        an exported csv file or a list of jobs"""
        self.search(query)
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
        y_vector = pd.read_csv(y, index_col=0)
        full_df = y_vector.append(df, ignore_index=True)
        return full_df

    def get_tfidf(self, df):
        self.vectorizer.fit(df['jobs'])
        transformed_model = self.vectorizer.transform(df['jobs'])
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
        sorted_df = pd.DataFrame(full_df.iloc[indices]).set_index(np.arange(0,full_df.shape[0]))
        sorted_df['labels'] = np.zeros(full_df.shape[0])
        sorted_tfidf = pd.DataFrame(tfidf_df.iloc[indices]).set_index(np.arange(0,full_df.shape[0]))
        total_df = pd.concat([indices_df, sorted_df, sorted_distances_df, sorted_tfidf], axis=1)
        total_df.iat[0,4] = 10.0
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
            return self.convert_to_csv()
        total_distance = yes_remains.distances + yes_remains.distances_from_yes - no_remains.distances_from_no
        remains = yes_remains.copy()
        remains['total_distance'] = total_distance
        next_best_index = remains.total_distance.idxmin()
        return self.find_next_best(remains, next_best_index)

    def convert_to_csv(self):
        check_variable = input('Proceed? (yes / no)')
        if check_variable == 'yes':
            name = input('Enter name: ')
            self.df.to_csv('/data/%s.csv' % name)
        else:
            return self.df

    def transform(self, df):
        try:
            self.find_next_best(df)
        except ValueError:
            return self.convert_to_csv()

class PruneForest():
    def __init__(self, param=None):
        self.param = param

    def get_feature_importances(self, model):
        feature_importances = model.feature_importances_
        idxs = np.nonzero(feature_importances)[0]
        return idxs

    def get_reverse_term_dict(self, vectorizer):
        word_dict = vectorizer.vocabulary_
        reverse_dict = {value: key for key, value in word_dict.items()}
        return reverse_dict

    def get_word_list(self, reverse_dict, idxs):
        word_list = [reverse_dict[key] for key in list(idxs)]
        return word_list

    def get_vocabulary(self, model, vectorizer):
        indices = self.get_feature_importances(model)
        reverse_dict = self.get_reverse_term_dict(vectorizer)
        word_list = self.get_word_list(reverse_dict, indices)
        return word_list

class FitModel():
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words=CUSTOM_STOP)
        self.forest = RandomForestClassifier(n_estimators=2000, criterion='entropy', n_jobs=-1)
        self.grad_boost = GradientBoostingClassifier(learning_rate=0.001, n_estimators=500, subsample=0.5)
        self.pruned_forest = PruneForest()

    def get_Xy(self, name):
        df = pd.read_csv(name, index_col=0)
        culled_df = df[df.labels != 0.0]
        X = culled_df.iloc[1:, 1]
        y = culled_df.iloc[1:, 2]
        return X, y

    def fit_primary(self, X, y):
        self.vectorizer.fit(X)
        transformed_matrix = self.vectorizer.transform(X)
        tfidf_df = pd.DataFrame(transformed_matrix.toarray())
        self.forest.fit(tfidf_df, y)
        return self.forest, self.vectorizer

    def prune_forest(self, forest, vectorizer):
        vocabulary = self.pruned_forest.get_vocabulary(forest, vectorizer)
        return vocabulary

    def improve(self, X, vocabulary):
        imp_vectorizer = TfidfVectorizer(stop_words=CUSTOM_STOP, vocabulary=vocabulary)
        imp_vectorizer.fit(X)
        transformed_matrix = imp_vectorizer.transform(X)
        tfidf_df = pd.DataFrame(transformed_matrix.toarray())
        return tfidf_df

    def fit_secondary(self, X, y):
        return self.grad_boost.fit(X, y)

    def transform(self, name):
        X, y = self.get_Xy(name)
        forest, vectorizer = self.fit_primary(X, y)
        vocabulary = self.prune_forest(forest, vectorizer)
        tfidf_df = self.improve(X, vocabulary)
        return self.fit_secondary(tfidf_df, y), vocabulary




data = PreprocessData()
total_df = data.transform('data/GLASSTEST.csv', 'data/ETHANTEST.csv')
test_num = 0
index = 1
recommended_posting = pd.DataFrame(total_df.iloc[index, :]).T
prediction = Predict(total_df)
job_title = recommended_posting.iloc[0,1]
job_company = recommended_posting.iloc[0,2]
job_desc = recommended_posting.iloc[0,3]
pred = '...'

@app.route('/')
def index():
    global job_title
    global job_company
    global job_desc
    return render_template('index.html',
                            job_title = job_title,
                            job_company=job_company,
                            job_desc=job_desc,
                            prediction=pred)

@app.route('/handle_yes', methods=['POST'])
def handle_yes():
    global total_df
    global recommended_posting
    global job_title
    global job_company
    global job_desc
    original_index = int(recommended_posting['indices'])
    label_index = total_df[total_df['indices'] == original_index].index[0]
    total_df.iat[label_index,4] = 1.0
    remains, next_best_index = find_next_best()
    recommended_posting = pd.DataFrame(remains.iloc[next_best_index, :]).T
    job_title = remains.iloc[next_best_index, 1]
    job_company = remains.iloc[next_best_index, 2]
    job_desc = remains.iloc[next_best_index, 3]
    return render_template('index.html',
                            job_title = job_title,
                            job_company=job_company,
                            job_desc=job_desc,
                            prediction=pred)

@app.route('/handle_no', methods=['POST'])
def handle_no():
    global total_df
    global recommended_posting
    global job_title
    global job_company
    global job_desc
    original_index = int(recommended_posting['indices'])
    label_index = total_df[total_df['indices'] == original_index].index[0]
    total_df.iat[label_index,4] = -1.0
    remains, next_best_index = find_next_best()
    recommended_posting = pd.DataFrame(remains.iloc[next_best_index, :]).T
    job_title = remains.iloc[next_best_index, 1]
    job_company = remains.iloc[next_best_index, 2]
    job_desc = remains.iloc[next_best_index, 3]
    return render_template('index.html',
                            job_title = job_title,
                            job_company=job_company,
                            job_desc=job_desc,
                            prediction=pred)

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

@app.route('/convert_to_csv', methods=['POST'])
def convert_to_csv():
    global total_df
    total_df.to_csv('~/galvanize/capstone/Ember-Job-Recommender/data/labeled_data.csv')
    return render_template('index.html',
                            job_title = job_title,
                            job_company=job_company,
                            job_desc=job_desc,
                            prediction=pred)
@app.route('/predict', methods=['POST'])
def predict():
    global total_df
    global job_title
    global job_company
    global job_desc
    global pred
    global test_num
    model = FitModel()
    grad_model, vocabulary = model.transform('~/galvanize/capstone/Ember-Job-Recommender/data/labeled_data.csv')
    final_jobs = remove_dups('data/GLASSTEST.csv', 'data/HOTTEST.csv')
    job_title = final_jobs.iloc[test_num, 0]
    job_company = final_jobs.iloc[test_num,1]
    job_desc = final_jobs.iloc[test_num, 2]
    X_test = [final_jobs.iloc[test_num, 2]]
    X_tfidf = model.improve(X_test, vocabulary)
    pred = grad_model.predict_proba(X_tfidf)
    formated_string = "%.2f" % (pred[0][1]*100) + "% Approval Prediction"
    test_num += 1
    return render_template('index.html',
                            job_title = job_title,
                            job_company=job_company,
                            job_desc=job_desc,
                            prediction=formated_string)

def remove_dups(train, test):
    train_df = pd.read_csv(train, index_col=0)
    test_df = pd.read_csv(test, index_col=0)
    final_jobs = test_df.copy()
    for test_job in test_df.jobs.values:
        for train_job in train_df.jobs.values:
            if test_job == train_job:
                final_jobs.drop(index=final_jobs[final_jobs.jobs == test_job].index[0], inplace=True)
    return final_jobs

@app.route('/get_linked', methods=['POST', 'GET'])
def get_linked():
    print("it worked")


class Main():
    def __init__(self, param=None):
        self.param = param

    def transform(self):
        li = LinkedinScraper()
        li.transform()
        glass = ScrapeGlass()
        query = input('Enter Job Field: ')
        glass.transform(query)
        data = PreprocessData()
        total_df = data.transform('../data/PIPETEST.csv', '../data/LINKTEST.csv')
        prediction = Predict(total_df)
        complete_df = prediction.transform(total_df)
        fit_model = FitModel()
        model = fit_model.transform('../data/LABELEDTEST.csv')
        return model



if __name__ == '__main__':
    pass
