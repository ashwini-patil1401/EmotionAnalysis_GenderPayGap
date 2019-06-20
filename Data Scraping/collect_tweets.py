from twython import Twython
import pandas as pd


#add your credentials here
TWITTER_APP_KEY = 'z2h1szyWoTKUvTgWt29Fk7zEh' 
TWITTER_APP_KEY_SECRET = 'NkrYCRA0GwSlgOh2DFQA973pg0rMT6UnkYTjOoHUa8hOjtaZ4I' 
TWITTER_ACCESS_TOKEN = '191310138-icISy4fetKHp3q7ChqwNiUFKoEEHu7dOXLCBXlEw'
TWITTER_ACCESS_TOKEN_SECRET = 'isQWJwJEiblQAqHVcMBag5cUJ3jV8qRMwjQxdjYUBE1di'

t = Twython(app_key=TWITTER_APP_KEY, 
            app_secret=TWITTER_APP_KEY_SECRET, 
            oauth_token=TWITTER_ACCESS_TOKEN, 
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

hashtags_list = ["womenintech", "womeninstem"]

for query_tag in hashtags_list:
	search = t.search(q='#'+query_tag, count=100)
	#search = t.search(q='#'+query_tag, since_id = 8.29977280629838E+017)
	#search = t.search(q='#'+query_tag, until = '2017-07-01')
	tweets = search['statuses']
	df = pd.DataFrame()

	for tweet in tweets:
		tweet_row = pd.Series([tweet['id_str'], tweet['text']])
		df = df.append(tweet_row, ignore_index=True)
	
	with open(query_tag+".csv", 'w') as fh:
                df.to_csv(fh)

	print("#"+query_tag+"created in: "+query_tag+".csv")

