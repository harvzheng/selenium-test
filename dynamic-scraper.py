from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

base_url = "https://twitter.com/"
account = "realDonaldTrump"
num_tweets = 100

driver = webdriver.Firefox()
driver.get(base_url + account)
driver.implicitly_wait(10)

def is_retweet(tweet):
  return "Retweeted" in tweet

class Tweet:
  def __init__(self, text, time):
    self.text = text
    self.time = time
  def __eq__(self, other):
    return self.text == other.text and self.time == other.time
  def __hash__(self):
    return hash(self.text) + hash(self.time)

def parse_tweet(tweet):
  s = tweet.splitlines()
  s.pop()
  s.pop()
  s.pop()
  s.pop(0)
  s.pop(0)
  s.pop(0)
  s.pop(0)
  return " ".join(s).strip()

start = time.time()
print("starting...")

output = open('raw.csv', mode='w')
output = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
output.writerow(['text'])

def scroll_down(driver, num_tweets, tweets_memoized):

  # Get scroll height.
  last_height = driver.execute_script("return document.body.scrollHeight")
  while len(tweets_memoized) < num_tweets:
    tweets = driver.find_elements_by_tag_name("article")
    for tweet in tweets:
      tweets_memoized.add(tweet.text)
      output.writerow([tweet.text])

      # Scroll down to the bottom.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load the page.
    time.sleep(2.5)

    # Calculate new scroll height and compare with last scroll height.
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:

        break

    last_height = new_height

  
tweets_memoized = set()
scroll_down(driver, num_tweets, tweets_memoized)
end = time.time()
print("finished!")
print(f"time: {end - start}")

tweets_parsed = set()
for tweet in tweets_memoized:
  if not is_retweet(tweet):
    num = tweet.count("\n")
    if num > 6:
      tweet = parse_tweet(tweet)
      tweets_parsed.add(tweet)

output = open('%s.csv' %account, mode='w')
output = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
output.writerow(['text'])

for tweet in tweets_parsed:
  output.writerow([tweet])


driver.close()