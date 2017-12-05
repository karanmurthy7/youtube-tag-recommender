
# coding: utf-8

# In[1]:


import pandas as pd
import json
import numpy as np
import nltk
from nltk.corpus import stopwords
import re
import gensim
import math


# In[2]:


global AVG_TAGS_PER_VIDEO, US_CA_GB_TOKEN_CORPUS, US_VIDEOS_DF, US_FINAL_DF
global CA_VIDEOS_DF, CA_FINAL_DF, GB_VIDEOS_DF, GB_FINAL_DF, US_CA_GB_FINAL_DF


# In[3]:


#get rid of the punctuations and set all characters to lowercase
RE_PREPROCESS = r'\W+|\d+' #the regular expressions that matches all non-characters

#get rid of punctuation and make everything lowercase
#the code belows works by looping through the array of text
#for a given piece of text we invoke the `re.sub` command where we pass in the regular expression, a space ' ' to
#subsitute all the matching characters with
#we then invoke the `lower()` method on the output of the re.sub command
#to make all the remaining characters
#the cleaned document is then stored in a list
#once this list has been filed it is then stored in a numpy array


# In[4]:


RE_REMOVE_URLS = r'http\S+'


# In[5]:


def processFeatures(desc):
    try:
        desc = re.sub(RE_REMOVE_URLS, ' ', desc)
        return re.sub(RE_PREPROCESS, ' ', desc)
    except:
        return " "


# In[6]:


def processDataFrame(data_frame, country_code='US'):
    data_frame.sort_values(by=['video_id', 'trending_date'], ascending=True, inplace=True)
    grouped_videos = data_frame.groupby(['video_id']).last().reset_index()

    #Reading categories from the json file depending on country_code
    json_location = './data/' + country_code +'_category_id.json'
    with open(json_location) as data_file:
        data = json.load(data_file)
    categories = []
    for item in data['items']:
        category = {}
        category['category_id'] = int(item['id'])
        category['title'] = item['snippet']['title']
        categories.append(category)

    categories_df = pd.DataFrame(categories)
    # Merging videos data with category data
    final_df = grouped_videos.merge(categories_df, on = ['category_id'])
    final_df.rename(columns={'title_y': 'category', 'title_x': 'video_name'}, inplace=True)

    # Creating a features column that consists all features used for prediction.
    # Also creating a corpus column that consists of all data required to train the model.
    final_df['video_features'] = ''
    final_df['video_corpus'] = ''

    if final_df['video_name'].astype(str) is not None:
        final_df['video_features'] += final_df['video_name'].astype(str)

    if final_df['channel_title'].astype(str) is not None:
        final_df['video_features'] += final_df['channel_title'].astype(str)

    if final_df['description'].astype(str) is not None:
        final_df['video_features'] += final_df['description'].astype(str)

    final_df['video_corpus'] += final_df['video_features']
    if final_df['tags'].astype(str) is not None:
        final_df['video_corpus'] += final_df['tags'].astype(str)


    final_df['video_features'] = final_df['video_features'].apply(processFeatures)
    final_df['video_corpus'] = final_df['video_corpus'].apply(processFeatures)
    return final_df


# In[7]:


def removeNonEngAndStopwords(documents):
    stopwords_list = stopwords.words('english')
    processed_corpus = []
    for document in documents:
        processed_document = []
        for word in document.split():
            try:
                if word not in stopwords_list and word.encode(encoding='utf-8').decode('ascii'):
                    processed_document.append(word)
            except UnicodeDecodeError:
                # Can log something here
                pass
        processed_corpus.append(processed_document)
    return processed_corpus


# In[8]:


def processCorpus(feature_corpus):
    feature_corpus = [comment.lower() for comment in feature_corpus]
    processed_feature_corpus = removeNonEngAndStopwords(feature_corpus)
    return processed_feature_corpus


# In[9]:


def trainModel(token_corpus, model_name = 'word2vec_model.w2v'):
    model = gensim.models.Word2Vec(sentences=token_corpus, min_count=1, size = 32)
    model.train(token_corpus, total_examples=model.corpus_count, epochs=model.iter)
    model.save(model_name)
    return model


# In[19]:


def recommendTags(word2vec_model, input_words = ['trump', 'president'], number_of_tags = 10, model_name = 'word2vec_model.w2v'):
    global US_CA_GB_TOKEN_CORPUS
    tags = []

    try:
        word2vec_model = gensim.models.Word2Vec.load(model_name)
        tags = word2vec_model.most_similar(positive=input_words, topn=number_of_tags)
    except FileNotFoundError:
        word2vec_model = trainModel(US_CA_GB_TOKEN_CORPUS, model_name)
        try:
            tags = word2vec_model.most_similar(positive=input_words, topn=number_of_tags)
        except:
            US_CA_GB_TOKEN_CORPUS.append(input_words)
            word2vec_model.build_vocab(US_CA_GB_TOKEN_CORPUS, update=True)
            word2vec_model.train(US_CA_GB_TOKEN_CORPUS, total_examples=word2vec_model.corpus_count, epochs=word2vec_model.iter)
            word2vec_model.save(model_name)
            tags = word2vec_model.most_similar(positive=input_words, topn=number_of_tags)
    except:
        US_CA_GB_TOKEN_CORPUS.append(input_words)
        word2vec_model.build_vocab(US_CA_GB_TOKEN_CORPUS, update=True)
        word2vec_model.train(US_CA_GB_TOKEN_CORPUS, total_examples=word2vec_model.corpus_count, epochs=word2vec_model.iter)
        word2vec_model.save(model_name)
        tags = word2vec_model.most_similar(positive=input_words, topn=number_of_tags)

    return tags


# In[20]:


def calculateAvgTagsPerVideo():
    total_tags = 0
    for tag_list in US_CA_GB_FINAL_DF['tags'].values:
        total_tags += len(tag_list.split('|'))
    return math.ceil(total_tags/len(US_CA_GB_FINAL_DF))


# Running the algorithm for US, CA, and GB videos

# In[21]:


def initializeAndFetchRecommendations(video_name = None, channel_title = None, video_category = None, description = None):
    global US_VIDEOS_DF, US_FINAL_DF, CA_VIDEOS_DF, CA_FINAL_DF, GB_VIDEOS_DF, GB_FINAL_DF
    global US_CA_GB_FINAL_DF, US_CA_GB_FINAL_DF, AVG_TAGS_PER_VIDEO, US_CA_GB_TOKEN_CORPUS
    US_VIDEOS_DF = pd.read_csv('./data/USvideos.csv')
    US_FINAL_DF = processDataFrame(US_VIDEOS_DF, country_code='US')

    CA_VIDEOS_DF = pd.read_csv('./data/CAvideos.csv')
    CA_FINAL_DF = processDataFrame(CA_VIDEOS_DF, country_code='CA')

    GB_VIDEOS_DF = pd.read_csv('./data/GBvideos.csv')
    GB_FINAL_DF = processDataFrame(GB_VIDEOS_DF, country_code='GB')

    US_CA_GB_FINAL_DF = pd.concat([US_FINAL_DF, CA_FINAL_DF, GB_FINAL_DF])
    US_CA_GB_FINAL_DF.reset_index(inplace=True)

    US_CA_GB_TOKEN_CORPUS = processCorpus(US_CA_GB_FINAL_DF['video_corpus'].values)
    US_CA_GB_FINAL_DF['video_features'] = processCorpus(US_CA_GB_FINAL_DF['video_features'].values)
    US_CA_GB_FINAL_DF['video_corpus'] = US_CA_GB_TOKEN_CORPUS

    AVG_TAGS_PER_VIDEO = calculateAvgTagsPerVideo()
    word2vec_model = None

    input_list = []
    if (video_name is not None or channel_title is not None or
        video_category is not None or description is not None):
        frontEndInput = frontEndInput = video_name + ' ' + channel_title + ' ' +  video_category + ' ' + description + ' '
        for word in frontEndInput.split(' '):
            if word not in stopwords.words('english') and len(word.strip()) > 0:
                input_list.append(word.lower())

    if input_list != []:
        return recommendTags(word2vec_model, input_words=input_list,
                         number_of_tags=AVG_TAGS_PER_VIDEO,
                         model_name = 'word2vec_model.w2v')

    return recommendTags(word2vec_model, input_words=['trump', 'president'],
                         number_of_tags=AVG_TAGS_PER_VIDEO,
                         model_name = 'word2vec_model.w2v')


# In[22]:
