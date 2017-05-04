from bson.objectid import ObjectId
from datetime import timedelta, datetime

from crawler.main import EntityProcessingThread
from test import MongoBaseTest, TestComment, TestSubmission

class CrawlerTest(MongoBaseTest):

  def test_entity_processing(self):
    start_time = datetime.utcnow() - timedelta(seconds = 1)
    insertion_comments = [TestComment('test_comment%s' % i) \
      for i in range(10)]
    insertion_submissions = [TestSubmission('test_submission%s' % i) \
      for i in range(10)]
    
    comments_ept = EntityProcessingThread('test', 'test_subreddit', \
      'comment', insertion_comments)
    comments_ept.mongoClient = self.mongo
    comments_ept.start()
    
    submissions_ept = EntityProcessingThread('test', 'test_subreddit', \
      'submission', insertion_submissions)
    submissions_ept.mongoClient = self.mongo
    submissions_ept.start()

    comments_ept.join()
    submissions_ept.join()

    end_time = datetime.utcnow() + timedelta(seconds = 1)
    res = self.mongo.get_entities('test_subreddit', \
      ObjectId.from_datetime(start_time), ObjectId.from_datetime(end_time))
    assert res['count'] == 20
    assert len(res['results']) == 20

    desired_items = [
      {u'subreddit': u'test_subreddit',
       u'text': u'test_comment%s' %i,
       u'type': u'comment'} for i in range(10)
    ] + [
      {u'subreddit': u'test_subreddit',
       u'text': u'test_submission%s' %i,
       u'type': u'submission'} for i in range(10)
    ]
    assert sorted(res['results'], key=lambda x: x['text']) == desired_items

if __name__ == '__main__':
  unittest.main()
