# %% [markdown]
# # Imports

# %%
import os
import re
import glob
import emoji
import pandas as pd
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

# %% [markdown]
# # Reading chat files

# %%
chatsFolder = "./chats"
lang = "sp"

mediaMessage = {
    "eng":"<media omitted>",
    "sp":"<multimedia omitido>" 
}

# %% [markdown]
# We get every .txt file in the chats folder and save it onto a list

# %%
chatList = []

for file in glob.glob(".\chats\*.txt"):
    chatList.append(file)

#chatList

# %% [markdown]
# Read the text in a file (in this case, the first .txt file)

# %%
with open(chatList[0],encoding="utf-8") as f:
  textsList = f.read()
  textsList = textsList.split('\n')

#textsList

# %% [markdown]
# # Data Cleaning

# %% [markdown]
# We will start by separating the user and date from the message.

# %% [markdown]
# We first define the regular expression or pattern our messages will follow, which will be:
# * [D]D/[M]M/[YY]YY HH:MM - User: Message

# %%
messagePattern = r"(\d{1,2}/\d{1,2}/\d{2,4}\s\d{1,2}:\d{2})\s-\s([^:]*):\s(.*)"

# %% [markdown]
# So, we will have the following groups:
# 1. Date and Hour
# 2. User
# 3. Message

# %% [markdown]
# Next, We create a dataframe whose columns will correspond with each group and print the number of messages. 
# 
# **Note:** You can only export up to 40000 messages when you are not including media attachments (and 10000 if you include them). 

# %%
users = []
dates = []
messages = []

for text in textsList:
    res = re.match(messagePattern, text)
    if res:
        date = res.group(1)
        #If the year has length 2, we reformat it
        dates.append(res.group(1))
        users.append(res.group(2))
        messages.append(res.group(3).lower())

df = pd.DataFrame({"user":users, "date": dates, "message":messages})

print("Number of messages in the chat:", len(df))

# %% [markdown]
# Save the messages as a string

# %%
messages = " ".join(messages)

# %% [markdown]
# Format the date as datetime object

# %%
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%y %H:%M")

# %% [markdown]
# We remove all the media messages, depending on the language

# %%
media = df[df["message"] == mediaMessage[lang]]
df.drop(media.index, inplace=True)
#media.groupby("user")["message"].count().sort_values(ascending=False)

# %%
media.head()

# %%
df.head()

# %%
print("Number of media shared in the chat: ", len(media))
print("Which makes up for a ", "{:.2f}".format(100*(len(media)/(len(media)+len(df)))) ,"% of the total number of messages in the chat. ")

# %%
media.head(10)

# %% [markdown]
# We reset the index and get a preview of the dataframe

# %%
df.reset_index(inplace=True, drop=True)

df.head(10)

# %% [markdown]
# # Chat Statistics

# %% [markdown]
# Number of messages per user

# %%
df.groupby("user")["message"].count().sort_values(ascending=False)

# %% [markdown]
# Message length by user

# %%
messagesByUser = df.groupby("user")["message"].apply(lambda x: "".join(x)).reset_index()
messagesByUser["len"] = messagesByUser["message"].str.len()
messagesByUser

# %%
type(messagesByUser)

# %% [markdown]
# Most commonly used emojis

# %%
emojisCounter = Counter()
emojisIter = map(lambda y: y, emoji.EMOJI_DATA.keys())
regex_set = re.compile('|'.join(re.escape(em) for em in emojisIter))

# %%
for index, row in messagesByUser.iterrows():
  emojis_found = regex_set.findall(row['message'])
  for emoji_f in emojis_found:
    emojisCounter[emoji_f] +=1

# %%
for item in emojisCounter.most_common(10):
  print(f'{item[0]} - {item[1]}')

# %%
spanishStopwords = ["a","con","de","desde","en","y","o","que","le","lo","la","de","el","del","más","se","por","pero","con","https","s","status","<multimedia omitido>","multimedia","omitido"]

stopwords = STOPWORDS.update(spanishStopwords)

wordcloud = WordCloud(width = 1000, height = 800, 
                background_color ='white').generate(messages) 

wordcloud.to_image()


