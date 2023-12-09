import pandas as pd
import re
import string

df_true = pd.read_csv('true_uncleaned.csv')
df_false = pd.read_csv('fake_uncleaned.csv')

def clean_date(df):
    df['month'] = df['date'].apply(lambda x: x.split(' ')[0]) 
    df['month'] = df['month'].apply(lambda x: month_converter.get(x))
    df['year'] = df['date'].apply(lambda x: int(x.split(' ')[2]))
    df['day'] = df['date'].apply(lambda x: int(x.split(' ')[1].replace(',', '')))
    
def remove_space(df, column, space):
    df[column] = df[column].apply(lambda x: x.replace(space, ' '))
    df[column] = df[column].apply(lambda x: x[1:] if x.startswith(' ') else x)
    
month_converter = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12,
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12,
    }


##CLEANING THE TRUE DATA

#Cleaning the date
clean_date(df_true)

#Droping the 'subject'
df_true.drop(['subject'], axis=1, inplace=True)
df_false.drop(['subject'], axis=1, inplace=True)

##CLEANING THE FAKE DATA

#Cleaning the date
month = df_false['date'].apply(lambda x: x.split(' ')[0] if ' ' in x else x.split('-')[1])
month = month.apply(lambda x: month_converter.get(x))

day = df_false['date'].apply(lambda x: x.split(' ')[1].replace(',', '') if ' ' in x else x.split('-')[0])
links = []
for i in range(0, len(day)):
    if len(day[i]) >=3:
        links.append(i)
day.drop(links, axis=0, inplace=True)
day = day.apply(lambda x:int(x))

month.drop(links, axis=0, inplace=True)
df_false.drop(links, axis=0, inplace=True)

year = df_false['date'].apply(lambda x: int(x.split(' ')[2]) if ' ' in x else 2018)

#Renaming the axis of the series
day.rename('day', inplace=True)
year.rename('year', inplace=True)
month.rename('month', inplace=True)

df_false = pd.concat([df_false, month, year, day], axis=1)
df_false = df_false.reset_index(drop=True)

##REMOVING THE UNCLEANED DATE
df_true.drop('date', axis=1, inplace=True)
df_false.drop('date', axis=1, inplace=True)

##SEPARATING THE TRUE AND FALE DATA USING A CLASS
df_true['class'] = 1
df_false['class'] = 0

## REMOVE DUPLICATES
print('Size of df_true: ', df_true.shape)
print('Size of df_false: ', df_false.shape)
df_true.drop_duplicates(subset=['text'], inplace=True)
df_false.drop_duplicates(subset=['text'], inplace=True)
print('New Size of df_true: ', df_true.shape)
print('New Size of df_false: ', df_false.shape)
df_false = df_false.reset_index(drop=True)
df_true = df_true.reset_index(drop=True)

##DATA FOR MANUAL TESTING
manual_fake = df_false.tail(10)
for i in range(17448, 17438, -1):
    df_false.drop([i], axis=0, inplace=True)
    
manual_true = df_true.tail(10)
for i in range(21191, 21181, -1):
    df_true.drop([i], axis=0, inplace=True)
    
manual = pd.concat([manual_fake, manual_true], axis = 0)

##CONCATING THE TRUE AND FALSE DATASETS
df = pd.concat([df_true, df_false], axis=0)

##REMOVING THE NULL VALUES AND SPACES
null_values = df[df['text'] == ' '].index
df.drop(null_values, axis=0, inplace=True)

null_values = df[df['title'] == ' '].index
df.drop(null_values, axis=0, inplace=True)

##REMOVING THE SPECIAL CHARACTERS
def word_drop(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('\\W', ' ', text)
    text = re.sub('https?://\S+|www\.\S+', ' ', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    
    return text

df['title'] = df['title'].apply(word_drop)
df['text'] = df['text'].apply(word_drop)
manual['title'] = manual['title'].apply(word_drop)
manual['text'] = manual['text'].apply(word_drop)

remove_space(df, 'title', '    ')
remove_space(df, 'title', '   ')
remove_space(df, 'title', '  ')
remove_space(df, 'text', '    ')
remove_space(df, 'text', '   ')
remove_space(df, 'text', '  ')
remove_space(manual, 'title', '    ')
remove_space(manual, 'title', '   ')
remove_space(manual, 'title', '  ')
remove_space(manual, 'text', '    ')
remove_space(manual, 'text', '   ')
remove_space(manual, 'text', '  ')

df['text'] = df['text'].apply(lambda x: x.replace('u s', 'usa'))
df['title'] = df['title'].apply(lambda x: x.replace('u s', 'usa'))
manual['text'] = manual['text'].apply(lambda x: x.replace('u s', 'usa'))
manual['title'] = manual['title'].apply(lambda x: x.replace('u s', 'usa'))
df['text'] = df['text'].apply(lambda x: x.replace('u s a', 'usa'))
df['title'] = df['title'].apply(lambda x: x.replace('u s a', 'usa'))
manual['text'] = manual['text'].apply(lambda x: x.replace('u s a', 'usa'))
manual['title'] = manual['title'].apply(lambda x: x.replace('u s a', 'usa'))

print(df.isnull().sum())
df.dropna()
print(df.isnull().sum())

##RE-INDEXING
df = df.reset_index(drop=True)
manual = manual.reset_index(drop=True)

##CHECKING THE FINAL SIZE
print('Last Size of df_true: ', df_true.shape)
print('Last Size of df_false: ', df_false.shape)
print('Last Size of df: ', df.shape)

##EXPORTING THE 'CLEANED' DATA
df.to_csv('dataset.csv')
manual.to_csv('manual_testing.csv')