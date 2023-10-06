import gdown
import argparse
import re

def extract_file_id(url):
    pattern = r'/d/(.*?)/view'
    match = re.search(pattern, url)
    extracted_string = match.group(1)
    final_url = f"https://drive.google.com/uc?id={extracted_string}"

    return final_url

def validate_url(url):
    pattern = r'^https://drive\.google\.com/file/d/[^/]+/view.*$'

    if re.match(pattern, url):
        return url
    else:
        return ValueError

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download the weights for the LLM')
    parser.add_argument('--url', required=True, help="Enter the URL of the zip file to download the weights.You can get it by sharing, the file on google drive and copying the link with the permission open 'Anyone can view'", type=validate_url)
    parser.add_argument('--output', help="The name of the file you want the downloaded zip to be saved as.")
    args = parser.parse_args()
    print(args)

    gdown.download(extract_file_id(args.url), args.output, quiet=False)
