#!/usr/bin/python
import psycopg2

# SETUP CONNECTION TO NEWS DB
try:
    conn = psycopg2.connect("dbname='news'")
    print ("Connected to news database")
except:
    print ("Unable to connect")

print
cur = conn.cursor()

# QUERY TOP 3 MOST POPULAR ARTICLES OF ALL TIME
cur.execute(
    "select title||' - '||cast(count(*)::int as text)||' views' as count "
    "from articles, log where "
    "articles.slug=substring(log.path from 10) group by articles.title order "
    "by count desc limit 3;")
results = cur.fetchall()
print ("The most popular three articles of all time are:")
for i in results:
    i = str(i)
    print i.replace('(', '') \
        .replace(')', '') \
        .replace("'", "") \
        .replace('"', '') \
        .replace(',', '')
print

# QUERY MOST POPULAR AUTHORS AND LIST THEM IN ORDER BY VIEWS
cur.execute(
    "select authortotals.name||' - '||cast(count(*)::int as text)||' views' "
    "as views from authortotals, "
    "log where authortotals.slug = substring(log.path from 10) group by "
    "authortotals.name order by views desc")
results = cur.fetchall()
print ("The most popular article authors are:")
for i in results:
    i = str(i)
    print i.replace('(', '').replace(')', '').replace("'", "").replace(',', '')
print

# QUERY NO. OF DAYS WITH OVER A 1% ERROR RATE
cur.execute(
    "select to_char(date::date, 'Mon DD, YYYY - ')||cast((round(percent,"
    "2)::double precision) as text)||'%' from "
    "logpercent where percent > 1.0")
results = cur.fetchall()
print ("On these days more than 1% of requests led to errors:")
for i in results:
    i = str(i)
    print i.replace('(', '').replace(')', '').replace("'", "").replace(',', '')
