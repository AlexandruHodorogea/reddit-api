from bson.objectid import ObjectId
import json
import time

from test import ServerBaseTest, TestComment, TestSubmission

class ServerTest(ServerBaseTest):

  def seed(self):
    self.seed_timestamp = int(time.time() - 60)
    insertion_comments = [TestComment('test_comment%s' % i) \
      for i in range(10)]
    insertion_comments.extend([TestComment('test_comment%s keyword' % i) \
      for i in range(2)])
    insertion_submissions = [TestSubmission('test_submission%s' % i) \
      for i in range(10)]
    insertion_submissions.extend([TestSubmission('test_submission%s keyword' % i) \
      for i in range(2)])
    for entity in insertion_submissions:
      self.mongo.insert_submission('test_subreddit', entity)
    for entity in insertion_comments:
      self.mongo.insert_comment('test_subreddit', entity)

    additional_comments = [TestComment('extra%s' % i) \
      for i in range(10)]
    additional_submission = [TestSubmission('extra%s' % i) \
      for i in range(10)]
    for subreddit in ['test_subreddit2', 'sbred', 'other_subredit']:
      for entity in additional_submission:
        self.mongo.insert_submission(subreddit, entity)
      for entity in additional_comments:
        self.mongo.insert_comment(subreddit, entity)
    self.after_seed_timestamp = int(time.time() + 60)

  def test_item_get(self):
    self.seed()
    rv = self.app.get('/items/?subreddit=%s&from=%s&to=%s' \
      % ('test_subreddit', self.seed_timestamp, self.after_seed_timestamp))
    response = json.loads(rv.data.decode("utf-8") )
    assert rv.status_code == 200
    assert response['data']['count'] == 24
    assert len(response['data']['results']) == 24 


  def test_item_keywords_get(self):
    self.seed()
    rv = self.app.get('/items/?subreddit=%s&from=%s&to=%s&keyword=%s' \
      % ('test_subreddit', self.seed_timestamp, self.after_seed_timestamp, 'keyword'))
    response = json.loads(rv.data.decode("utf-8") )
    assert rv.status_code == 200
    assert response['data']['count'] == 4
    assert len(response['data']['results']) == 4 