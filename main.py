from datetime import datetime
from inc.DataDownloader import DataDownloader
from inc.RenderPlot import RenderPlot


dl = DataDownloader()
monthly_stats = dl.get_monthly_stats_cached()

print("Datapoints:", len(monthly_stats))
#print(monthly_stats)

render = RenderPlot(monthly_stats)
render.render(
    RenderPlot.GROUP_MONTH,
    chart_type=RenderPlot.CHART_LINE,
    date_from='2023-01-01 00:00:00',
    #date_from='2022-01-01 00:00:00',  # twitter takeover-range
    #date_to='2023-09-01 00:00:00', # easier to see test range
    date_to=str(datetime.now().date()) + " 00:00:00"
)
