# FSND-Log-Analysis

# Log Analysis project

## Stack used includes:
* Git Bash console to load a Vagrant Ubuntu Linux VM and SSH into it
* Python 2.7
* PSQL

## Views
This project uses views to manage postgresql query returns into manageable chunks of formatted data suitable for troubleshooting analysis, business reports, analytics, etc.
In this case, the news database contains web traffic logs and will be used to report a series of traffic analytics questions.

## The questions that must be answered are:
**1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.**

Example:

* "Princess Shellfish Marries Prince Handsome" — 1201 views<br>
* "Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views<br>
* "Political Scandal Ends In Political Scandal" — 553 views

**2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.**

Example:

* Ursula La Multa — 2304 views
* Rudolf von Treppenwitz — 1985 views
* Markoff Chaney — 1723 views
* Anonymous Contributor — 1023 views

**3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer back to this lesson if you want to review the idea of HTTP status codes.)**

Example:

* July 29, 2016 — 2.5% errors


### The views can be reproduced as follows:
#### Name: authortotals
```
CREATE VIEW authortotals AS
SELECT authors.name,
       articles.slug,
       authors.id
FROM authors,
     articles
WHERE authors.id = articles.author
ORDER BY authors.name;
```

#### Name: logcounts
```
CREATE VIEW logcounts AS
SELECT logdailytotals."time" AS date,
       logdailytotals.count AS total,
       logdailyerrors.count AS errors
FROM logdailytotals,
     logdailyerrors
WHERE logdailytotals."time" = logdailyerrors."time";
```

#### Name: logdailytotals
```
CREATE VIEW logdailytotals AS
SELECT log."time"::date AS "time",
       count(log.status) AS COUNT
FROM log
GROUP BY (log."time"::date);
```
#### Name: logdailyerrors
```
CREATE VIEW logdailyerrors AS
SELECT log."time"::date AS "time",
       count(log.status) AS COUNT
FROM log
WHERE log.status !~~ '200 OK'::text
GROUP BY (log."time"::date)
ORDER BY (log."time"::date);
```
#### Name: logpercent
```
CREATE VIEW logpercent AS
SELECT logcounts.date,
       logcounts.errors::numeric / logcounts.total::numeric * 100::numeric AS percent
FROM logcounts;
```
