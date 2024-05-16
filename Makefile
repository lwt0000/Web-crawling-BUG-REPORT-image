crawl:
	@echo "Crawling bug reports..."
	@cd bug_report_scraper && scrapy crawl bug_spider -O ../data/bug_reports.json

download:
	@echo "Downloading buggy images..."
	python3 download.py

clean:
	rm -rf data/bug_reports.json
	rm -rf data/images