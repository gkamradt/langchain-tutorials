import tweepy
from airtable import Airtable
from datetime import datetime, timedelta
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate, SystemMessagePromptTemplate, AIMessagePromptTemplate, HumanMessagePromptTemplate
import schedule
import time
from dotenv import load_dotenv
import os

load_dotenv()

# load your Twitter and Airtable API keys (preferably from environment variables or a config file)
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "YourKey")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "YourKey")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "YourKey")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "YourKey")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "YourKey")
TWEET_RESPONSE_LIMIT = 30 # How many tweets to respond to each wake up

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY", "YourKey")
AIRTABLE_BASE_KEY = os.getenv("AIRTABLE_BASE_KEY", "YourKey")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "YourKey")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YourKey")

class TwitterBot:
    def __init__(self):
        self.twitter_api = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN,
                                         consumer_key=TWITTER_API_KEY,
                                         consumer_secret=TWITTER_API_SECRET,
                                         access_token=TWITTER_ACCESS_TOKEN,
                                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
                                         wait_on_rate_limit=True)

        self.airtable = Airtable(AIRTABLE_BASE_KEY, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY)
        self.twitter_me_id = self.get_me_id()
        self.response_limit = TWEET_RESPONSE_LIMIT
        self.llm = ChatOpenAI(temperature=.5, openai_api_key=OPENAI_API_KEY)
        self.mentions_found = 0
        self.mentions_replied = 0
        self.mentions_replied_errors = 0
        
    def execute_replies(self):
        print (f"Starting Job: {datetime.utcnow().isoformat()}")
        self.respond_to_mentions()
        print (f"Finished Job: {datetime.utcnow().isoformat()}, Found: {self.mentions_found}, Replied: {self.mentions_replied}, Errors: {self.mentions_replied_errors}")

    def get_me_id(self):
        return self.twitter_api.get_me()[0].id
    
    def get_mention_parent_tweet(self, referenced_tweets):
        for tweet in referenced_tweets:
            if tweet.type == 'replied_to':
                parent_tweet = self.twitter_api.get_tweet(tweet.id).data
                return parent_tweet
        return None

    def get_mentions(self):
        # If doing this in prod make sure to deal with pagination
        # Get current time in UTC
        now = datetime.utcnow()

        # Subtract 2 hours to get the start time
        start_time = now - timedelta(hours=2)

        # Convert to required string format
        start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        return self.twitter_api.get_users_mentions(id=self.twitter_me_id,
                                                   start_time=start_time_str,
                                                   expansions=['referenced_tweets.id'],
                                                   tweet_fields=['created_at']).data

    def respond_to_mentions(self):
        mentions = self.get_mentions()
        self.mentions_found = len(mentions)

        for mention in mentions[:self.response_limit]:
            # Check to see if there is a parent tweet
            mentioned_parent_tweet = self.get_mention_parent_tweet(mention.referenced_tweets)
            
            # If not just move on and don't respond
            if mentioned_parent_tweet is not None:
                mentioned_parent_tweet_text = mentioned_parent_tweet.text
                
                # Check to see if you've already responded to a mention. If not, then respond
                if not self.already_responded(mention.id):
                    self.respond_to_mention(mention, mentioned_parent_tweet_text)

    def already_responded(self, mention_tweet_id):
        records = self.airtable.get_all(view='Grid view')

        for record in records:
            if record['fields'].get('mentioned_tweet_id') == str(mention_tweet_id):
                return True
        return False

    def respond_to_mention(self, mention, mentioned_parent_tweet_text):
        
        response_text = self.generate_response(mentioned_parent_tweet_text)
        
        try: 
            response_tweet = self.twitter_api.create_tweet(text=response_text, in_reply_to_tweet_id=mention.id)
            self.mentions_replied += 1
        except Exception as e:
            print (e)
            
            self.mentions_replied_errors += 1
            return
            
        self.airtable.insert({
            'mentioned_tweet_id': str(mention.id),
            'mentioned_tweet_parent_text': mentioned_parent_tweet_text,
            'tweet_response_id': response_tweet.data['id'],
            'tweet_response_text': response_text,
            'tweet_response_created_at' : datetime.utcnow().isoformat(),
            'mentioned_at' : mention.created_at.isoformat()
        })

    def generate_response(self, mentioned_parent_tweet_text):
        # It would be nice to bring in information about the links, pictures, etc.
        # But out of scope for now
        system_template = """
            You are a smart mad scientist from silicon valley.
            Your goal is to give a concise prediction about a piece of text from the user.

            - Include specific examples of old tech if they are relevant
            - Respond in under 200 characters
            - Your prediction should be given in an active voice and be opinionated
            - If you don't have an answer, say, "Sorry, my magic 8 ball isn't working right now 🔮"
            - Your response should be a prediction
            - Your tone should be serious sarcastic
            - Respond in one short sentence

            The user will give you a piece of text to respond to
        """
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

        human_template="{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        # get a chat completion from the formatted messages
        final_prompt = chat_prompt.format_prompt(text=mentioned_parent_tweet_text).to_messages()
        response = llm(final_prompt).content
        
        return response
    
def job():
    print(f"Job executed at {datetime.utcnow().isoformat()}")
    bot = TwitterBot()
    bot.execute_replies()
    
    
if __name__ == "__main__":
    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)