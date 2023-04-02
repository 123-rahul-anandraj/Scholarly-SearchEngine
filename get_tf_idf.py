# -*- coding: utf-8 -*-
"""get_tfidf.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_9pmwDzqorzD2K3efQL2mb8JTpYWjZHH
"""

import json
import sys
import pandas as pd
sys.path.append('../helper_functions/')
from common_functions import get_id

# list of number of professors in each csv
csv_sizes = list(pd.read_csv(r'E:/BE-FinalYear-CSE-XIE/FinalYr_BE_Project/Final_Scholarly/scholarly (1)/scholarly/Re-cleaned-pr0f_data_cleaned/metadata.csv', header=None)[0])

# read TF-IDF scores from JSON file
with open(r'E:/BE-FinalYear-CSE-XIE/FinalYr_BE_Project/Final_Scholarly/scholarly (1)/scholarly/Re-cleaned-pr0f_data_cleaned/tf_idf_scores_topic_and_paper_full.json') as f:
    tf_idf_score = json.load(f)

def get_tf_idf_list(parsed_query,n=99999999999):
    '''
    Input:
    > parsed_query - search query parsed using get_tokenized_words()
    > n - number of results to return (default: 99999999999)
    Output:
    > docs_list[:n] - list of global IDs of top n professors based on
    TF-IDF score computed using parsed_query
    '''
    global tf_idf_score       
    docs_dict = {}           

    # Computing TF-IDF scores of all documents(professors) that contain at least 
    # one word/term from the parsed query in it. If a document contains multiple terms
    # from the query, then the scores are added.       
    
    # The below code is optimized because tf-idf score is computed for only those doc 
    # that contain atleast one term from the query, the tf-idf score of other documents would be zero
    for term in parsed_query:
        for file_index in range(len(csv_sizes)):
            for prof_index in range(csv_sizes[file_index]):
                doc = get_id(file_index, prof_index)
                key = term+'_'+str(doc)
                if key in tf_idf_score:
                    if doc not in docs_dict:
                        docs_dict[doc] = tf_idf_score[key]
                    else:
                        docs_dict[doc] += tf_idf_score[key]    

    # create list of results containing tuples of form (prof id, score)
    docs_list = []
    for doc, score in docs_dict.items():
        docs_list.append([doc, score])

    # sort in decreasing order of score
    docs_list.sort(key = lambda x: x[1], reverse=True)

    # remove scores from the list
    for i in range(len(docs_list)):
        docs_list[i] = docs_list[i][0]

    # return first n results
    return docs_list[:n]