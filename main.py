from inc.DataDownloader import DataDownloader

dl = DataDownloader()
monthly_stats = dl.get_monthly_stats()
print("Datapoints:", len(monthly_stats))

