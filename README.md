# Data Engineer application answers

This repository contains answers for the Python and SQL questions in the take home assignment.

The [video walkthrough](https://youtu.be/p711B9lx83E) accompanies these answers.

## Question 1 Python product search

Requires Python 3.10 or newer, internet access, and the packages in `requirements.txt`.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scrape_products.py "external harddrive"
```

Pass a search term to the program. It requests the first MD Computers search results page and prints each listed product's name, displayed price, and URL as CSV. To save the output, append `> products.csv` to the last command. CSV handles commas in product names and is easy to inspect or import. Product images and later result pages are outside the requested scope.

The program reports request failures instead of presenting an empty product list as a successful scrape. It uses a browser style HTTP client because MD Computers blocked basic Python requests during testing. The example search returned 20 product rows on 21 October 2026.

## Question 2 SQL

The answers are in [`rfam_queries.sql`](rfam_queries.sql). In the assignment, SQL item 4 says "Write the SQL query for this." I read that as the instruction to write the family pagination query described in item 3, so there is no separate fourth query.

Run the file with a MySQL client against [Rfam's public read only database](https://docs.rfam.org/en/latest/database.html).

```sh
mysql --user rfamro --host mysql-rfam-public.ebi.ac.uk --port 4497 --database Rfam < rfam_queries.sql
```

The queries count distinct Acacia taxonomy names, find the wheat species with the longest `rfamseq` sequence, and return page 9 of families ordered by their longest linked sequence. Each page has 15 rows, so page 9 starts after 120 rows. `rfamseq.length` gives the full sequence length. `full_region` links families to sequences.

On 21 October 2026, the first two queries returned **326** and **Triticum durum (durum wheat)** (`LT934116.1`, length **836,514,780**). The final query passed the database's query plan check but did not finish within a four minute test. Runtime and results may change when Rfam updates its public database.

## Question 3 Unix shell

I primarily used Windows and have recently moved to Ubuntu. I used the assignment's option to skip the Unix shell question.
