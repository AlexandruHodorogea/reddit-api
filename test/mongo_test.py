from bson.objectid import ObjectId
from datetime import timedelta


from test import MongoBaseTest, TestComment, TestSubmission
class MongoTest(MongoBaseTest):

  def test_basic_insertion(self):
    self.mongo.collection.insert_one({'test':'test'})
    res = list(self.mongo.collection.find())
    assert len(res) == 1
    assert len(res[0]) == 2
    assert res[0].get('test') == 'test'

  def test_comment_insertion(self):
    tc = TestComment()
    io_obj = self.mongo.insert_comment('test_subreddit',tc)
    insert_time = io_obj.inserted_id.generation_time
    a = insert_time - timedelta(seconds = 1)
    b = insert_time + timedelta(seconds = 1)
    res = self.mongo.get_entities('test_subreddit', \
      ObjectId.from_datetime(a), ObjectId.from_datetime(b))

    assert res == {
      'count': 1,
      'results': [{u'subreddit': u'test_subreddit',
        u'text': u'test_text',
        u'type': u'comment'}]
    }

  def test_submission_insertion(self):
    ts = TestSubmission()
    io_obj = self.mongo.insert_submission('test_subreddit',ts)
    insert_time = io_obj.inserted_id.generation_time
    a = insert_time - timedelta(seconds = 1)
    b = insert_time + timedelta(seconds = 1)
    res = self.mongo.get_entities('test_subreddit', \
      ObjectId.from_datetime(a), ObjectId.from_datetime(b))

    assert res == {
      'count': 1,
      'results': [{u'subreddit': u'test_subreddit',
        u'text': u'test_text',
        u'type': u'submission'}]
    }

if __name__ == '__main__':
  unittest.main()