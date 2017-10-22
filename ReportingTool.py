#!/usr/bin/python3
# Logs Analysis Project - Udacity

import psycopg2


# Connect to database
def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except connectionError:
        print("Could not connect to database")

# 1. What are the most popular three articles of all time?
# Which articles have been accessed the most?
# Present this information as a sorted list with the most popular article
# at the top.
# Example:
# "Princess Shellfish Marries Prince Handsome" — 1201 views
# "Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
# "Political Scandal Ends In Political Scandal" — 553 views


def popularArticles():
    db, cursor = connect()
    popular_articles = '''
                  SELECT title, path_count FROM articles JOIN (SELECT
                  replace(path, '/article/', '') AS path_conv,
                  count(path) AS path_count FROM log GROUP BY path_conv) AS
                  converted_count_table ON articles.slug
                  = path_conv GROUP BY title, path_count
                  ORDER BY path_count DESC LIMIT 3
                  '''
    cursor.execute(popular_articles)
    print("Most popular articles:")
    for (title, path_count) in cursor.fetchall():
        print("    {} - {} views".format(title, path_count))
    print("-" * 70)
    cursor.close()
    db.close()


popularArticles()

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
    db, cursor = connect()
    popular_authors = '''
                  SELECT name, sum(path_count) FROM (SELECT name, path_count
                  FROM (SELECT replace(path, '/article/', '') AS path_conv,
                  count(path) AS path_count FROM log GROUP BY path_conv) AS
                  path_conv JOIN (SELECT name, title, slug FROM authors JOIN
                  articles ON articles.author = authors.id) AS author_title ON
                  path_conv = slug GROUP BY name, path_count) AS
                  name_path_count WHERE name = name GROUP BY name
                  order by sum DESC
                  '''
    cursor.execute(popular_authors)
    print("Most popular authors:")
    for (name, sum) in cursor.fetchall():
        print("    {} - {} views".format(name, sum))
    print("-" * 70)
    cursor.close()
    db.close()


popularAuthors()

# 3. On which days did more than 1% of requests lead to errors? The log table
# includes a column
# status that indicates the HTTP status code that the news site sent
# to the user's browser. (Refer
# back to this lesson if you want to review the idea of HTTP status codes.)
# Example:
# July 29, 2016 — 2.5% errors


def errorDays(entries_view, errors_view):
    db, cursor = connect()
    entries_view = entries_view
    errors_view = errors_view
    # COMMENT1
    # I've inserted the 2 below views (entries_view and errors_view) in data
    # base "newsdata.sql". However, when I run code, I get the error:
    # File "ReportingTool.py", line 125, in <module>
    # errorDays(entries_view, errors_view)
    # NameError: name 'entries_view' is not defined
    # CREATE view entries_view as select to_char(time, 'Month DD, YYYY') as
    # date1, count(id) as visitors_daily from log group by date1"
    # CREATE view errors_view as select to_char(time, 'Month DD, YYYY') as
    # date2, count(status) as error_daily from log where status = '404 NOT
    # FOUND' group by date2"
    # This is just for demoing, that query works (when uncommenting queries):
    # total_entries = '''
    #               CREATE view entries_view as select to_char(time,
    #               'Month DD, YYYY') as date1, count(id) as visitors_daily
    #               from log group by date1
    #            '''
    # cursor.execute(total_entries)
    # error_entries = '''
    #            CREATE view errors_view as select to_char(time, 'Month
    #            DD, YYYY') as date2, count(status) as error_daily from
    #            log where status = '404 NOT FOUND' group by date2
    #            '''
    # cursor.execute(error_entries)

    error_days = '''
            SELECT date1, diff FROM (SELECT date1,
            (cast(error_daily AS decimal) / cast(visitors_daily AS
            decimal) * 100) AS diff from entries_view JOIN errors_view ON
            date1 = date2 GROUP BY date1, diff) AS diff_table WHERE
            diff > 1 GROUP BY date1, diff ORDER BY diff DESC
            '''
    cursor.execute(error_days)
    print("Days with more than 1% '404s':")
    for (date1, diff) in cursor.fetchall():
        print("    {} - {:.2f}%".format(date1, diff))
    cursor.close()
    db.close()


errorDays(entries_view, errors_view)
