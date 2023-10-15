from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tag import pos_tag

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer, PorterStemmer
import pandas as pd

import re

from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
import numpy as np

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')

def extract_keywords(text, num_keywords=3):
    words = word_tokenize(text.lower())

    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    filtered_words = [word for word in filtered_words if word.isalnum() and word not in {"able"}]

    tagged_words = pos_tag(filtered_words)

    # Filter for nouns and adjectives
    keywords = [word for word, pos in tagged_words if pos in ('NN', 'NNS', 'JJ', 'JJR', 'JJS')]

    tagged_words2 = pos_tag(filtered_words, tagset="universal")
    keywords2 = [word for word, pos in tagged_words2 if pos in ('NOUN', 'VERB')]

    fdist = FreqDist(keywords)
    fdist2 = FreqDist(keywords2)

    top_keywords = [word for word, freq in fdist.most_common(num_keywords)]
    top_keywords2 = [word for word, freq in fdist2.most_common(num_keywords)]

    return set(top_keywords)

def group_by_value(input_dict):
    result_dict = {}
    
    for key, value in input_dict.items():
        if value in result_dict:
            result_dict[value].append(key)
        else:
            result_dict[value] = [key]
    
    return result_dict

def keyword_grouping(issueVsKeyword,sorted_keyword_document_dict, issues_summary, number_of_keywords):
    issue_summ_cpy = issues_summary.copy()
    keyword_issue_mapping = {}
    
    for keyword, issue_ids in sorted_keyword_document_dict.items():
        for issue_id in issue_ids:
          nWords = []
          
          for keyword2, issue_ids2 in sorted_keyword_document_dict.items():
            if issue_id in issue_ids2:
              nWords.append(keyword2)
            if (len(nWords) == number_of_keywords) or (len(nWords) >= len(issueVsKeyword[issue_id])):
              break

          if(issue_id in issue_summ_cpy):
            keyword_issue_mapping[issue_id] = " ".join(nWords)
            del issue_summ_cpy[issue_id]

    
    return group_by_value(keyword_issue_mapping)

def keywordsMapping(issues,max_number_of_keywords):
  issues_summary = issues.copy()

  all_keywords = set()

  #Extract keywords for each document and attach them
  for issue in issues:
    summary = issues[issue]
    issues[issue] = extract_keywords(summary,num_keywords=5)

  issueVsKeyword = issues

  keyword_document_dict = {}

  for issue in issues:
      document_id = issue
      keywords = issues[issue]

      for keyword in keywords:
          if keyword in keyword_document_dict:
              keyword_document_dict[keyword].append(document_id)
          else:
              keyword_document_dict[keyword] = [document_id]

  sorted_keyword_document_dict = dict(sorted(keyword_document_dict.items(), key=lambda item: len(item[1]), reverse=True))
  
  keywords_summary_map_full = {}
  
  for keywordCount in range (1,max_number_of_keywords+1):
    result = keyword_grouping(issueVsKeyword,sorted_keyword_document_dict, issues_summary, keywordCount)

    keywords_summary_map = {}
    
    # Iterate through the sorted_keyword_document_dict
    for keyword, document_ids in result.items():
        grouped_issues = []

        for document_id in document_ids:
            issue_summary = issues_summary[document_id]
            grouped_issues.append(issue_summary)

        keywords_summary_map[keyword] = grouped_issues
        
    keywords_summary_map_full[keywordCount] = keywords_summary_map
        

  return keywords_summary_map_full




def checkTeam(request):
    request_data = request.body

    # Parse the JSON string into a Python dictionary
    data = json.loads(request_data)
    data = json.loads(data)

    mappedData = keywordsMapping(data,5)

    
    print(mappedData)
    return JsonResponse(mappedData)

