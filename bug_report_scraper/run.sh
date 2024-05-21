#!/bin/bash

# Read the CSV file
CSV_FILE="start_urls.csv"
echo "Script is running..."

# Check if the CSV file exists
if [[ ! -f "$CSV_FILE" ]]; then
    echo "CSV file $CSV_FILE not found!"
    exit 1
fi

# Loop through each line in the CSV file
{
    read  # Skip the header line
    while IFS=, read -r raw_url raw_game_name
    do
        # Debug statement to show the raw data being read
        echo "Raw URL: $raw_url, Raw Game Name: $raw_game_name"

        # Remove the single quotes around the URL and game name
        url=$(echo $raw_url | tr -d "'")
        game_name=$(echo $raw_game_name | tr -d "'")

        # Remove any leading or trailing spaces
        url=$(echo $url | xargs)
        game_name=$(echo $game_name | xargs)

        # Display a message for the current game being crawled
        echo "Crawling bug reports for $game_name..."

        # Construct the output file name
        output_file="../data/bug_reports_${game_name}.json"

        # Debug statement to show the output file name
        echo "Output file: $output_file"

        # Run the Scrapy spider with the start URL and game name
        scrapy crawl bug_spider -a start_urls=$url -a game_name=$game_name -O $output_file

        # Check if the last command was successful
        if [[ $? -ne 0 ]]; then
            echo "Scrapy crawl failed for $url"
            # Exit the script on failure (optional)
            # exit 1
        else
            echo "Scrapy crawl succeeded for $url"
        fi

    done
} < "$CSV_FILE"

echo "Crawling completed."
