# Python version: #!/usr/bin/python3
# Logs Analysis Project - Udacity

import psycopg2
# Connect to database
conn = psycopg2.connect("dbname=news")
# Open a cursor to perform database operations
cur = conn.cursor()

# 1. What are the most popular three articles of all time?
# Which articles have been accessed the most?
# Present this information as a sorted list with the most popular article
# at the top.
# Example:
# "Princess Shellfish Marries Prince Handsome" — 1201 views
# "Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
# "Political Scandal Ends In Political Scandal" — 553 views
# Joins tables articles and log, on converted path with slug.
cur.execute("select title, path_count from articles join (select " +
            "replace(path, '/article/', '') as path_conv, count(path) as " +
            "path_count from log group by path_conv) as " +
            "converted_count_table on articles.slug " +
            "= path_conv group by title, path_count " +
            "order by path_count desc limit 3")
results = cur.fetchall()
print(results)

# 2. Who are the most popular article authors of all time? That is, when you
# sum up all of the articles each author has written, which authors get the
# most page views? Present this as a sorted list with the most popular author
# at the top.
# Example:
# Ursula La Multa — 2304 views
# Rudolf von Treppenwitz — 1985 views
# Markoff Chaney — 1723 views
# Anonymous Contributor — 1023 views
# Prints name of author and sum af hver author's views fra log.
cur.execute("select name, sum(path_count) from (select name, path_count " +
            "from (select replace(path, '/article/', '') as path_conv, " +
            "count(path) as path_count from log group by path_conv) as " +
            "path_conv join (select name, title, slug from authors join " +
            "articles on articles.author = authors.id) as author_title on " +
            "path_conv = slug group by name, path_count) as name_path_count " +
            "where name = name group by name order by sum desc")
results = cur.fetchall()
print(results)
# ALTERNATIVES SOLUTION WITH VIEWS (VIEWS NOT CREATED)
# Convert path in log to slug-format and count path
# cur.execute("select replace(path, '/article/', '') as path_conv, count(path)
# as path_count from log group by path_conv")
# results = cur.fetchall()
# print (results)
# Find authors and their articles
# cur.execute("select name, title from authors join articles on
# articles.author = authors.id group by name, title")
# results = cur.fetchall()
# print (results)
# Join above tables on articles.slug = path_conv
# cur.execute("select name, path_count from (select replace(path, '/article/',
# '') as path_conv, count(path) as path_count from log group by path_conv) as
# path_conv join (select name, title, slug from authors join articles on
# articles.author = authors.id) as author_title on path_conv = slug group
# by name, path_count order by path_count desc")
# results = cur.fetchall()
# print (results)
# Lastly, sum path_count where author = author.

# 3. On which days did more than 1% of requests lead to errors? The log table
# includes a column
# status that indicates the HTTP status code that the news site sent
# to the user's browser. (Refer
# back to this lesson if you want to review the idea of HTTP status codes.)
# Example:
# July 29, 2016 — 2.5% errors
# Step 1: Count all entries per date
cur.execute("create view entries_view as select " +
            "to_char(time, 'Month DD, YYYY') as date1, count(id) as " +
            "visitors_daily from log group by date1 ")
# Step 2: Count all 404s per date
cur.execute("create view errors_view as select " +
            "to_char(time, 'Month DD, YYYY') as date2, count(status) as " +
            "error_daily from log where status = '404 NOT FOUND' group by " +
            "date2")
# Step 3: Divide 404s with Entries and show dates with diff > 1%
cur.execute("select date1, diff from (select date1, " +
            "(cast(error_daily as decimal) / cast(visitors_daily as " +
            "decimal) * 100) as diff from entries_view join errors_view on " +
            "date1 = date2 group by date1, diff) as diff_table where diff > " +
            "1 group by date1, diff order by diff desc")
results = cur.fetchall()
print(results)
# Close connections
cur.close()
conn.close()
