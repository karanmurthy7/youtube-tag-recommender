# YouTube Tag Recommender
## Introduction:
Every day, 30 million users visit YouTube on an average, and approximately 5 billion videos are viewed every day. When about 300 hours of video content are uploaded every minute on YouTube, it’s not surprising if a video gets lost in the limbo. With an ever-increasing number of YouTube uploaders, it’s of paramount importance for one to be ahead of the game and incorporate smart strategies to make one’s video(s) relevant. That’s where tagging comes into the picture. Tags are one of the most important ways for an uploader to maximize viewership. A set of relevant tags can help the YouTube search engine optimization to cherry pick such videos and place them much higher on the search results.
 
## Data Description:
For this project, we considered the top 800 videos in the Trending section of YouTube for the months September through November 2017 in the US, UK and Canada. The corpus consisted of 8996 videos, out of which around 3029 were unique. Below are some interesting features of the dataset:
•	Video name (Approximately 51 characters on an average per video name)
•	Channel name (Approximately 13 characters on an average per video name)
•	Category (15 unique categories including 'Education', 'Comedy', 'Sports', 'Pets & Animals', 'News & Politics', 'Entertainment', 'Music', 'Howto & Style', 'People & Blogs', 'Science & Technology', ‘Film & Animation', 'Gaming', 'Autos & Vehicles', 'Travel & Events', 'Shows')
•	Description (Approximately 400 characters on an average per video description)
•	Tags (19 tags on an average per video)

 
## Data Munging:
Since a video could have been in the top 800 in Trending section for multiple days, it made sense to retain only the latest entry, with the latest statistics. Stop words were removed from the dataset using the NLTK package. The column containing the URL links of a given video was removed as it was deemed irrelevant to the analysis. The team decided to focus only on English words, and as such non-English words were removed using UTF-8 encoding.
 
## Methods and Approach:
 Our approach to recommend tags was basically feed the entire video corpus (video name, video description, tags, channel title, video category) to one of the following three models and recommend tags based on cosine similarity of the input typed by the user with the text in the corpus. For the purposes of similarity, our threshold was 0.75, meaning all matches above 0.75 would be considered and the top 19 tags would be retrieved. We decided on the number 19 as it is the average number of tags per video in our dataset. For model building, we considered the following three approaches but later narrowed down on one approach:
### 1.	TFIDF Vectorizer and cosine similarity
a.	In this approach, we used a TF-IDF vectorizer to vectorize the entire corpus and use cosine similarity to match the user’s input with the words in the corpus. But this approach disappointed us as TF-IDF calculates similarity only on the basis of the TF-IDF scores of words and is not able to infer relationships using context of the word in a sentence.

### 2.	Doc2Vec and cosine similarity
a.	In this approach, we used Doc2Vec to vectorize the entire corpus and use cosine similarity to match the user’s input with sentences (documents) in the corpus. But even this approach disappointed as Doc2Vec converts an entire sentence into a vector and then calculates similarity. We wanted some model that would use the words in a sentence to calculate similarity.

### 3.	Word2Vec and cosine similarity
a.	In this approach, we used Word2Vec to vectorize the entire corpus and use cosine similarity to match the user’s input with words in the corpus. This approach gave us results that looked promising. For instance, when we input words such as “How to bake a cake?”, we get the following output:
Tags: #sweet, #baking, #syrup, #nutella, #ingredients, #bake, #macarons
This prompted us to use word2vec as our model to recommend tags. 
