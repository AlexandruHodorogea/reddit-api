SETTINGS = {
  'env': 'local',
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


try:
  from config.settings_local import set_locals

  set_locals(SETTINGS)
except:
  print('no SETTINGS_LOCAL')