from  urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

#creating a function to check out the details from individual users
def fetch_stats(selected_user,df):
     if  selected_user != "Overall":
         df = df[df["user"] == selected_user]  # to show a user has done how many messages

    #to checkout the number of messages shared
     num_messages = df.shape[0] #showing number of messages
     words = []
     for message in df["message"]:
        words.extend(message.split())
     extract = URLExtract()
    #to check out the links shared
     links = []
     for message in df["message"]:
        links.extend(extract.find_urls(message))

     num_media = df[df["message"] == "<Media omitted>\n"].shape[0]
     return num_messages, len(words) ,num_media,len(links)



#checking the most active users
def  most_active_users(df):
    x = df["user"].value_counts().head()
    df = round((df["user"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={"index": "name", "user": "percent"})  # to show the active users in percent form
    return x,df



#creating a word cloud to see which words are used more and used less
def create_word_cloud(selected_user,df):
    f = open("B:\Machine Learning Projects\Whatsapp Chat Analysis\stopwords.txt", "r")
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    temp = df[df["user"] != "Group_Notification"]
    temp = temp[temp["message"] != "<Media omitted>\n"]
    def remove_stopwords(message):
       y=[]
       for word in message.lower.split():
           if word not in stop_words:
               y.append(word)
       return " ".join(y)

    wc = WordCloud(width =350 , height=350,min_font_size=10,background_color="white")
    df_wc = wc.generate(df["message"].str.cat(sep=" ")) #to create word cloud we use generate function
    return df_wc



#Most used words
def common_words(selected_user,df):
    f = open("B:\Machine Learning Projects\Whatsapp Chat Analysis\stopwords.txt", "r")
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    # removing stopwords-->>>>
    temp = df[df["user"] != "Group_Notification"]
    temp = temp[temp["message"] != "<Media omitted>\n"]
    temp
    words = []
    for message in temp["message"]:
        for word in message.lower().split():  # making all words in lower case
            if word not in stop_words:
                words.append(word)  # appending words which are not in stopwords

    new_df =  pd.DataFrame(Counter(words).most_common(20))
    return new_df


#emojis checking
def emoji_check(selected_user,df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    emojis = []
    for message in df["message"]:  # to check if any message match with this unicode emiji then it will be ynder emojis list
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df



def daily_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    new_timeline = df.groupby("Only_Date").count()["message"].reset_index()
    return new_timeline



def week_activity(selected_user,df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df["DAY_NAME"].value_counts()


def month_activity(selected_user,df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df["month_name"].value_counts()



def activity_heatmap(selected_user,df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    df_heatmap = df.pivot_table(index="DAY_NAME", columns="Period", values="message", aggfunc="count").fillna(0)
    return df_heatmap