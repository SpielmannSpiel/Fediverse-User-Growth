import os
import json
import requests
from datetime import datetime
import matplotlib.pyplot as plt


class RenderPlot:
    # Class constants for grouping options
    GROUP_DAY = 'day'
    GROUP_WEEK = 'week'
    GROUP_MONTH = 'month'
    # Class constants for chart types
    CHART_BAR = 'bar'
    CHART_LINE = 'line'

    def __init__(self, data):
        """
        Initialize the renderer with the data.

        Parameters:
            data (list): A list of dictionaries, where each dictionary has
                         keys 'id', 'total_users', and 'date_checked'.
        """
        self.data = data

    def group_data(self, group_by=GROUP_DAY):
        """
        Group data by the specified time interval and summarize total_users.

        Parameters:
            group_by (str): The interval to group by. Options are GROUP_DAY,
                            GROUP_WEEK, or GROUP_MONTH.

        Returns:
            tuple: Two lists - (x_values, y_values) where x_values are the group labels
                   and y_values are the sums.
        """
        valid_options = {self.GROUP_DAY, self.GROUP_WEEK, self.GROUP_MONTH}
        if group_by not in valid_options:
            raise ValueError(f"Invalid group_by option '{group_by}'. Choose from {valid_options}.")

        groups = {}
        for record in self.data:
            try:
                dt = datetime.strptime(record['date_checked'], '%Y-%m-%d %H:%M:%S')
            except ValueError as ve:
                raise ValueError(f"Error parsing date '{record['date_checked']}': {ve}")

            if group_by == self.GROUP_DAY:
                key = dt.strftime('%Y-%m-%d')
            elif group_by == self.GROUP_WEEK:
                key = f"{dt.year}-W{dt.isocalendar()[1]:02d}"
            elif group_by == self.GROUP_MONTH:
                key = dt.strftime('%Y-%m')

            groups.setdefault(key, 0)
            groups[key] += record.get('total_users', 0)

        sorted_groups = sorted(groups.items(), key=lambda x: x[0])
        if sorted_groups:
            x_values, y_values = zip(*sorted_groups)
        else:
            x_values, y_values = [], []
        return list(x_values), list(y_values)

    def render(self, group_by=GROUP_DAY, chart_type=CHART_BAR):
        """
        Group the data by the specified interval, then render a chart using Matplotlib with XKCD style.

        Parameters:
            group_by (str): The interval to group by. Options are GROUP_DAY, GROUP_WEEK, or GROUP_MONTH.
            chart_type (str): The type of chart to render. Options are CHART_BAR or CHART_LINE.
        """
        valid_chart_types = {self.CHART_BAR, self.CHART_LINE}
        if chart_type not in valid_chart_types:
            raise ValueError(f"Invalid chart_type '{chart_type}'. Choose from {valid_chart_types}.")

        x_values, y_values = self.group_data(group_by)

        with plt.xkcd():
            fig, ax = plt.subplots(figsize=(10, 6))

            if chart_type == self.CHART_BAR:
                ax.bar(x_values, y_values, color='skyblue')
            elif chart_type == self.CHART_LINE:
                ax.plot(x_values, y_values, marker='o', linestyle='-', color='skyblue')

            ax.set_title(f'Total Users Grouped by {group_by.capitalize()} ({chart_type.capitalize()} Chart)')
            ax.set_xlabel(group_by.capitalize())
            ax.set_ylabel('Total Users')

            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()


if __name__ == "__main__":
    # Real sample data for testing
    sample_data = [
        {'id': 14429, 'total_users': 20, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14430, 'total_users': 4, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14293, 'total_users': 0, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14431, 'total_users': 4250, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14432, 'total_users': 1, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14433, 'total_users': 1, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14294, 'total_users': 4, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14295, 'total_users': 0, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14296, 'total_users': 0, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14297, 'total_users': 0, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14298, 'total_users': 1, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14299, 'total_users': 168571, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14300, 'total_users': 0, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14301, 'total_users': 0, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14302, 'total_users': 0, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14434, 'total_users': 132, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14303, 'total_users': 9, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14304, 'total_users': 0, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14305, 'total_users': 1, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14306, 'total_users': 1, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14307, 'total_users': 38, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14308, 'total_users': 258, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14309, 'total_users': 0, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14310, 'total_users': 39924, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14311, 'total_users': 1, 'date_checked': '2025-02-01 01:01:01'},
    ]

    # Fake data for testing
    sample_data_fake = [
        {'id': 14305, 'total_users': 10, 'date_checked': '2025-01-01 01:01:01'},
        {'id': 14306, 'total_users': 20, 'date_checked': '2025-01-01 01:01:01'},
        {'id': 14307, 'total_users': 30, 'date_checked': '2025-01-01 01:01:01'},
        {'id': 14308, 'total_users': 10, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14309, 'total_users': 10, 'date_checked': '2025-02-01 01:01:01'},
        {'id': 14310, 'total_users': 10, 'date_checked': '2025-02-01 01:01:01'},
    ]

    # Test 1: Render using the real sample data, grouped by month as a bar chart.
    print("Rendering real sample data grouped by month (Bar Chart):")
    renderer_real = RenderPlot(sample_data)
    renderer_real.render(group_by=RenderPlot.GROUP_DAY, chart_type=RenderPlot.CHART_BAR)

    # Test 2: Render using the fake sample data, grouped by month (default chart type is bar).
    print("Rendering fake sample data grouped by month (Bar Chart):")
    renderer_fake = RenderPlot(sample_data_fake)
    renderer_fake.render(group_by=RenderPlot.GROUP_MONTH)

    # Test 3: Line
    print("Rendering fake sample data grouped by month (Line Chart):")
    renderer_fake = RenderPlot(sample_data_fake)
    renderer_fake.render(group_by=RenderPlot.GROUP_MONTH, chart_type=RenderPlot.CHART_LINE)
