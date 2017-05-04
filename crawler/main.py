import json
from multiprocessing import Process
import threading

import praw

from config.settings import CRAWLER_CONFIG_FILE_PATH
from db import RedditMongoClient

class EntityProcessingThread(threading.Thread):
  def __init__(self, threadID, subreddit_name, task, generator):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.mongoClient = RedditMongoClient()
    self.generator = generator
    self.subreddit_name = subreddit_name
    self.task = task
  def run(self):
    for entity in self.generator:
      if self.task == 'comment':
        self.mongoClient.insert_comment(self.subreddit_name, entity)
      elif self.task == 'submission':
        self.mongoClient.insert_submission(self.subreddit_name, entity)
      else:
        raise Exception()


def process_subreddit(subreddit_name, subreddit):
  print "Starting process %s" % subreddit_name
  submissions_thread = None
  comments_thread = None
  try:
    submissions_thread = EntityProcessingThread \
      (subreddit_name + '_submissions', subreddit_name, \
        'submission', subreddit.stream.submissions())
    comments_thread = EntityProcessingThread \
      (subreddit_name + '_comments', subreddit_name, \
        'comment', subreddit.stream.comments())
    submissions_thread.start()
    comments_thread.start()
  except Exception as e:
    print "Error: unable to start thread on process %s" % subreddit_name
  if submissions_thread and comments_thread:  
    submissions_thread.join()
    comments_thread.join()  
  print "Thread finished on process %s" % subreddit_name

def get_targeted_subreddits():
  subreddits = [];
  with open(CRAWLER_CONFIG_FILE_PATH, 'r') as f:
    subreddits = json.load(f).get('subreddits', None);
  return subreddits

def run_all_processes():
  reddit = praw.Reddit('bot1', user_agent='UNIX:_J0flLV8M6CJUw:1.0.0')

  try:
    subreddits = get_targeted_subreddits()
  except:
    print("Failed to read config file from path %s" % CRAWLER_CONFIG_FILE_PATH)
    return

  processes = []
  if subreddits:
    for sr in subreddits:
      subreddit  = reddit.subreddit(sr)
      p = Process(target=process_subreddit, args=(sr, subreddit, ))
      p.start()
      processes.append(p)

  for p in processes:
    p.join()

if __name__ == '__main__':
  run_all_processes()


  


