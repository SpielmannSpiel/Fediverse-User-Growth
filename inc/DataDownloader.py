import os
import json
import requests


class DataDownloader:
    def __init__(self, url="https://api.fediverse.observer/", cache_file="data/monthly_growth.json"):
        self.url = url
        self.cache_file = cache_file
        # Ensure the directory for the cache file exists
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)

    def get_monthly_stats(self, force_download=False):
        # Check if cached data exists and force_download is not requested.
        if not force_download and os.path.exists(self.cache_file):
            print(f"Using cached data from {self.cache_file}")
            with open(self.cache_file, 'r') as f:
                cached_data = json.load(f)
            try:
                # Extract and return the relevant data
                return cached_data['data']['monthlystats']
            except KeyError:
                raise Exception("Cached data does not have the expected structure.")

        # GraphQL query to fetch the monthly stats.
        query = """
        {
          monthlystats{
            id
            total_users
            date_checked
          }
        }
        """

        response = requests.post(self.url, json={'query': query})
        if response.status_code == 200:
            data = response.json()
            # Save the fetched data to the cache file.
            with open(self.cache_file, 'w') as cache_file_handle:
                json.dump(data, cache_file_handle, indent=2)
            try:
                return data['data']['monthlystats']
            except KeyError:
                raise Exception("Fetched data does not have the expected structure.")
        else:
            raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

# Example usage:
if __name__ == "__main__":
    downloader = DataDownloader()
    try:
        # Set force_download to True to bypass the cache, or False to use cached data when available.
        monthly_stats = downloader.get_monthly_stats(force_download=False)
        print("Monthly Stats:", monthly_stats)
    except Exception as e:
        print("Error:", e)
