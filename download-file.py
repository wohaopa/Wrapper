import urllib.request

url_file = 'urls.txt'

with open(url_file, 'r') as file:
    urls = file.readlines()

for url in urls:
    url = url.strip()
    if not url:
        continue

    file_name = url.split('/')[-1]

    try:
        urllib.request.urlretrieve(url, file_name)
        print(f"File downloaded successfully and saved to {file_name}")

    except Exception as e:
        print(f"Failed to download {url}. Error: {e}")
