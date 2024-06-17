all: crawl download

crawl:
	@echo "Crawling images..."
	cd bug_report_scraper && chmod +x run.sh && ./run.sh

download:
	@echo "Downloading buggy images..."
	python3 download.py

clean:
	rm -rf data/*
	rm -rf data/images/*