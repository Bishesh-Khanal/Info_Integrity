import pickle
import pandas as pd

file_path = 'train_Uncleaned_ARXIV.pkl'

with open(file_path, 'rb') as file:
    loaded_data = pickle.load(file)
    
df_train = loaded_data.drop(['content_emotion', 'comments_emotion', 'emotion_gap', 'style_feature'], axis=1)

file_path = 'test_Uncleaned_ARXIV.pkl'

with open(file_path, 'rb') as file:
    loaded_data = pickle.load(file)
    
df_test = loaded_data.drop(['content_emotion', 'comments_emotion', 'emotion_gap', 'style_feature'], axis=1)

file_path = 'val_Uncleaned_ARXIV.pkl'

with open(file_path, 'rb') as file:
    loaded_data = pickle.load(file)
    
df_val = loaded_data.drop(['content_emotion', 'comments_emotion', 'emotion_gap', 'style_feature'], axis=1)

df_train['length'] = df_train['content'].apply(lambda x: len(x))
df_test['length'] = df_test['content'].apply(lambda x: len(x))
df_val['length'] = df_val['content'].apply(lambda x: len(x))

df = pd.concat([df_train, df_test, df_val], axis=0)
df['label'] = df['label'].apply(lambda x: int(x))
df = df[df['label'] == 0]
df.drop(['comments', 'category', 'length'], axis=1, inplace=True)
df.reset_index(inplace=True)
df.drop(['index'], axis=1, inplace=True)
df.to_csv('df_Fake_Arxiv.csv')