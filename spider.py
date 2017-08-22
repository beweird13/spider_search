import sys
import urllib.request
from bs4 import BeautifulSoup

about_this = """
This program performs a web spider search originating from a given URL to find connecting websites that contain given keywords.
"""

def process_page(url, keywords, depth, existing_list):
	if (depth == 0): return None

	return_urls = list()
	try:
		html = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(html, "html.parser")

		for word in keywords:
			if (soup.body.get_text().find(word)) == -1:
				return None

		return_urls.append(url)
		tags = soup('a')
		for tag in tags:
			href = tag.get('href', "")
			if ((href.startswith("http://") or href.startswith("https://")) and href not in existing_list and not href.endswith(".pdf")):
				urls = process_page(href, keywords, depth - 1, existing_list)
				if (urls != None):
					return_urls.extend(urls)
	except Exception as e:
		#print("Unable to open",e)
		return None

	return return_urls


if __name__ == "__main__":
	print(about_this)

	try:
		#for simplicity in testing, can forgo manual input entry and grab input from file
		if (len(sys.argv) == 2):
			filename = sys.argv[1]
			with open(filename, 'r') as f:
				url = f.readline().strip()
				if (not url.startswith("http://") and not url.startswith("https://")):
					raise Exception

				keywords_str = f.readline().strip()
				if (len(keywords_str) == 0):
					raise Exception
				keywords = keywords_str.split(',')

				depth = int(f.readline().strip())
				if (depth < 1):
					raise Exception			
			f.close()
		else:
			#normal use case
			url = input("Enter complete url (http://...): ").strip()
			if (not url.startswith("http://") and not url.startswith("https://")):
				raise Exception

			keywords_str = input("Enter comma seperated keywords: ").strip()
			if (len(keywords_str) == 0):
				raise Exception
			keywords = keywords_str.split(',')

			depth = int(input("Enter depth of search (including starting url): ").strip())
			if (depth < 1):
				raise Exception
	except Exception as e:
		print("Invalid input value")
		raise SystemExit

	print("Processing...")
	significant_urls = process_page(url, keywords, depth, list())
	for url in significant_urls:
		print(url)
