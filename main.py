from inc.DataDownloader import DataDownloader
from inc.RenderPlot import RenderPlot


dl = DataDownloader()
monthly_stats = dl.get_monthly_stats_cached()

print("Datapoints:", len(monthly_stats))
#print(monthly_stats)

render = RenderPlot(monthly_stats)
render.render(RenderPlot.GROUP_MONTH)
