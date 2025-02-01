import os
import json
import requests
from datetime import datetime


class DataDownloader:
    def __init__(self, url="https://api.fediverse.observer/", cache_file="data/monthly_growth.json"):
        self.url = url
        self.cache_file = cache_file
        # Ensure the directory for the cache file exists
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)

    def get_monthly_stats(self, force_download=False):
        """
        Fetch monthly stats from the API. If force_download is False and the cache file exists,
        the cached data is used.
        """
        if not force_download and os.path.exists(self.cache_file):
            print(f"Using cached data from {self.cache_file}")
            with open(self.cache_file, 'r') as f:
                cached_data = json.load(f)
            try:
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

    def get_monthly_stats_cached(self):
        """
        Return the monthly stats data, using the cached version if it was updated in the current month.
        If the cache is from a previous month, update it automatically.
        """
        need_update = True
        if os.path.exists(self.cache_file):
            mod_timestamp = os.path.getmtime(self.cache_file)
            mod_date = datetime.fromtimestamp(mod_timestamp)
            now = datetime.now()

            # Check if the cache file was modified in the same year and month as now.
            if mod_date.year == now.year and mod_date.month == now.month:
                need_update = False

        if need_update:
            print("Cache is outdated. Updating data...")
            return self.get_monthly_stats(force_download=True)
        else:
            print(f"Using up-to-date cached data from {self.cache_file}")
            with open(self.cache_file, 'r') as f:
                cached_data = json.load(f)
            try:
                return cached_data['data']['monthlystats']
            except KeyError:
                raise Exception("Cached data does not have the expected structure.")

