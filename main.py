# stdlib
import os
import argparse

# files
import cloud_storer as cloud
import xbox_sale_scraper as scrape

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'url',
        action='store',
        help='runs scrape_xbox_sale function, arg is the sale URL'
    )
    args = parser.parse_args()
    bucket = 'xbox_sale_scraper_results'
    results_fpath = scrape.scrape_xbox_sale(args.url)
    results_fname = os.path.basename(results_fpath)
    cloud.upload_blob(
        bucket,
        results_fpath,
        results_fname
    )
