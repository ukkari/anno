import os
import requests
from bs4 import BeautifulSoup

# List of URLs of the websites to scrape
urls = [
    'https://www.gikai.metro.tokyo.lg.jp/record/proceedings/2024-1/',
    'https://www.gikai.metro.tokyo.lg.jp/record/proceedings/2024-2/',
    'https://www.gikai.metro.tokyo.lg.jp/record/proceedings/2023-1/',
    'https://www.gikai.metro.tokyo.lg.jp/record/proceedings/2023-2/',
    'https://www.gikai.metro.tokyo.lg.jp/record/proceedings/2023-3/',
    'https://www.gikai.metro.tokyo.lg.jp/record/proceedings/2023-4/'
]

for url in urls:
    # Create the save directory if it doesn't exist
    save_dir = 'save'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Send a GET request to the website
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the <div class="contents" id="contents">
    contents_div = soup.find('div', {'class': 'contents', 'id': 'contents'})

    # Find all links within the specified <div>
    links = contents_div.find_all('a', href=True) if contents_div else []

    # Initialize a variable to store all link texts
    all_link_texts = ""

    # Iterate over each link
    for link in links:
        link_text = link.get_text()
        if "議事" in link_text:
            continue  # Ignore links whose text contains "議事"
        href = link['href']
        link_url = href if href.startswith('http') else url + href

        # Send a GET request to the link
        link_response = requests.get(link_url)
        link_response.raise_for_status()

        # Parse the HTML content of the link response
        link_soup = BeautifulSoup(link_response.content, 'html.parser')

        # Extract the contents within <div class="contents" id="contents">
        contents_div = link_soup.find('div', {'class': 'contents', 'id': 'contents'})
        link_text = contents_div.get_text() if contents_div else "No content found in the specified div."

        # Append the extracted text to the all_link_texts variable
        all_link_texts += link_text + "\n\n"

    # Extract the file name from the URL
    url_file_name = os.path.basename(url.rstrip('/'))

    # Create a filename based on the basename of the URL
    filename = os.path.join(save_dir, url_file_name + '.txt')

    # Save all the link texts to a single text file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(all_link_texts)

    print(f'Saved all content to {filename}')

