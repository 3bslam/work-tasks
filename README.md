# Books to Scrape



## Run

```
pip install requests beautifulsoup4
python scrape_books.py
```

## Here's the answer

1. What broke: the listing pages cut long titles short ("A Light in the …"), so I took the full title from the link instead of the visible text.
2. What took longer: the price came with a £ sign and the book links were relative, so I had to strip the price to a number and build full URLs.
3. Loading into SQL Server: 23 titles contain commas, which broke the columns until I used `FORMAT = 'CSV'` in `BULK INSERT`, and I converted `true`/`false` to `BIT` after loading.
4. If blocked after 50 requests: my script only sends 5 requests (one per listing page), so it wouldn't hit that limit unless I had to open each book's page.
5. In that case: I'd wait 1–3 seconds between requests, back off and retry on 429/503 errors, and cache pages to disk so reruns don't send the same requests again.
