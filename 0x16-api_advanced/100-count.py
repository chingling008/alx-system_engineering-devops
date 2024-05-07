#!/bin/python3
import praw

def get_words_from_title(title, word_list, word_counts):
  """
  Parses a title for keywords and updates a dictionary with counts.

  Args:
    title: The title of a Reddit post (str).
    word_list: A list of keywords to search for (list of str).
    word_counts: A dictionary to store counts of each keyword (dict of str: int).

  Returns:
    None
  """
  for word in word_list:
    # Ensure case-insensitive matching and avoid partial matches with punctuation
    if word.lower() in title.lower() and not (word.lower() + "." in title.lower() or word.lower() + "!" in title.lower() or word.lower() + "_" in title.lower()):
      word_counts[word.lower()] = word_counts.get(word.lower(), 0) + 1

def count_words(subreddit, word_list, after=None):
  """
  Recursively queries Reddit for hot articles, parses titles, and counts keywords.

  Args:
    subreddit: The name of the subreddit to query (str).
    word_list: A list of keywords to search for (list of str).
    after: A string to specify pagination after a previous request (str, optional).

  Returns:
    None
  """
 user_agent = "MyCustomScript v1.0 (by your_username)"

  reddit = praw.Reddit(client_id="",
                      client_secret="",
                      user_agent=user_agent)

  subreddit = reddit.subreddit(subreddit)
  hot_articles = subreddit.hot(limit=100, after=after)

  word_counts = {}
  for submission in hot_articles:
    get_words_from_title(submission.title, word_list, word_counts)

  # Base case: No more articles to process
  if not hot_articles.data.after:
    # Sort word counts by count (descending) and then alphabetically (ascending)
    sorted_counts = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))
    for word, count in sorted_counts:
      if count > 0:
        print(f"{word}: {count}")
    return

  # Recursive case: Fetch more articles and continue processing
  count_words(subreddit, word_list, hot_articles.data.after)
