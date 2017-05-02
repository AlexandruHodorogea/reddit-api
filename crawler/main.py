import json
from multiprocessing import Process
import threading

import praw

from config.settings import CRAWLER_CONFIG_FILE_PATH
from db import RedditMongoClient

class SubmissionsProcessingThread(threading.Thread):
  def __init__(self, threadID, subreddit_name, generator):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.mongoClient = RedditMongoClient(subreddit_name)
    self.generator = generator
  def run(self):
    for submission in self.generator:
      self.mongoClient.insert_submission(submission)


class CommentsProcessingThread(threading.Thread):
  def __init__(self, threadID, subreddit_name, generator):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.mongoClient = RedditMongoClient(subreddit_name)
    self.generator = generator
  def run(self):
    for comment in self.generator:
      self.mongoClient.insert_comment(comment)

def process_subreddit(subreddit_name, subreddit):
  print "Starting process %s" % subreddit_name
  submissions_thread = None
  comments_thread = None
  try:
    submissions_thread = SubmissionsProcessingThread \
      (subreddit_name + '_submissions', subreddit_name, \
        subreddit.stream.submissions())
    comments_thread = CommentsProcessingThread \
      (subreddit_name + '_comments', subreddit_name, \
        subreddit.stream.comments())
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


  


