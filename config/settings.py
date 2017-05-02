ENV = 'local'

SETTINGS = {
  'local': {
    'mongo': {
      'host': 'localhost',
      'port': 27017,
      'database': 'reddit',
    },
  },
  'test': {
    'mongo': {
      'host': 'localhost',
      'port': 27017,
      'database': 'reddit_test',
    }
  }
}


CRAWLER_CONFIG_FILE_PATH = 'config/subreddits.json'