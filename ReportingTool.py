#!/usr/bin/python3
# Logs Analysis Project - Udacity

import psycopg2


# Connect to database
def connect(query):
    try:
        db = psycopg2.connect(database="news")
        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        db.close()
        return result
    except Exception as e:
        print(e)
        exit(1)


# 1. What are the most popular three articles of all time?
# Which articles have been accessed the most?
# Present this information as a sorted list with the most popular article
# at the top.
# Example:
# "Princess Shellfish Marries Prince Handsome" — 1201 views
# "Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
# "Political Scandal Ends In Political Scandal" — 553 views
def popularArticles():
    popular_articles = '''
                  SELECT title, path_count FROM articles JOIN (SELECT
                  replace(path, '/article/', '') AS path_conv,
                  count(path) AS path_count FROM log GROUP BY path_conv) AS
                  converted_count_table ON articles.slug
                  = path_conv GROUP BY title, path_count
                  ORDER BY path_count DESC LIMIT 3
                  '''
    result = connect(popular_articles)
    print("Most popular articles:")
    for (title, path_count) in result:
        print("    {} - {} views".format(title, path_count))
    print("-" * 70)


# 2. Who are the most popular article authors of all time? That is, when you
# sum up all of the articles each author has written, which authors get the
# most page views? Present this as a sorted list with the most popular author
# at the top.
# Example:
# Ursula La Multa — 2304 views
# Rudolf von Treppenwitz — 1985 views
# Markoff Chaney — 1723 views
# Anonymous Contributor — 1023 views
def popularAuthors():
    popular_authors = '''
                  SELECT name, sum(path_count) FROM (SELECT name, path_count
                  FROM (SELECT replace(path, '/article/', '') AS path_conv,
                  count(path) AS path_count FROM log GROUP BY path_conv) AS
                  path_conv JOIN (SELECT name, title, slug FROM authors JOIN
                  articles ON articles.author = authors.id) AS author_title ON
                  path_conv = slug GROUP BY name, path_count) AS
                  name_path_count GROUP BY name
                  order by sum DESC
                  '''
    result = connect(popular_authors)
    print("Most popular authors:")
    for (name, sum) in result:
        print("    {} - {} views".format(name, sum))
    print("-" * 70)


# 3. On which days did more than 1% of requests lead to errors? The log table
# includes a column
# status that indicates the HTTP status code that the news site sent
# to the user's browser. (Refer
# back to this lesson if you want to review the idea of HTTP status codes.)
# Example:
# July 29, 2016 — 2.5% errors
def errorDays():
    error_days = '''
            SELECT to_char(date1, 'FMMonth FMDD, YYYY'), diff FROM (SELECT
            date1, (cast(error_daily AS decimal) / cast(visitors_daily AS
            decimal) * 100) AS diff from entries_view JOIN errors_view ON
            date1 = date2) AS diff_table WHERE
            diff > 1 ORDER BY diff DESC
            '''
    result = connect(error_days)
    print("Days with more than 1% '404s':")
    for (date1, diff) in result:
        print("    {} - {:.2f}%".format(date1, diff))


if __name__ == "__main__":
    popularArticles()
    popularAuthors()
    errorDays()
