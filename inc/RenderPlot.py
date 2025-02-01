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
        Also reads known events from data/known_events.json and annotates them on the plot.

        Parameters:
            group_by (str): The interval to group by. Options are GROUP_DAY, GROUP_WEEK, or GROUP_MONTH.
            chart_type (str): The type of chart to render. Options are CHART_BAR or CHART_LINE.
        """
        valid_chart_types = {self.CHART_BAR, self.CHART_LINE}
        if chart_type not in valid_chart_types:
            raise ValueError(f"Invalid chart_type '{chart_type}'. Choose from {valid_chart_types}.")

        # Get grouped data as x labels and corresponding sums
        x_values, y_values = self.group_data(group_by)
        # Use numeric positions for plotting
        positions = list(range(len(x_values)))
        # Create a mapping of group key to x position for annotation
        key_to_index = {key: i for i, key in enumerate(x_values)}

        with plt.xkcd():
            fig, ax = plt.subplots(figsize=(10, 6))

            # Plot based on the selected chart type
            if chart_type == self.CHART_BAR:
                ax.bar(positions, y_values, color='skyblue')
            elif chart_type == self.CHART_LINE:
                ax.plot(positions, y_values, marker='o', linestyle='-', color='skyblue')

            ax.set_title(f'Total Users Grouped by {group_by.capitalize()} ({chart_type.capitalize()} Chart)')
            ax.set_xlabel(group_by.capitalize())
            ax.set_ylabel('Total Users')
            ax.set_xticks(positions)
            ax.set_xticklabels(x_values, rotation=45)

            # Load known events from file and annotate them on the plot
            known_events = []
            known_events_path = os.path.join('data', 'known_events.json')
            try:
                with open(known_events_path, 'r') as f:
                    known_events = json.load(f)
            except Exception as e:
                print(f"Could not load known events from {known_events_path}: {e}")

            # Determine a y-position for annotations (use 95% of the current y-axis limit)
            ymax = max(y_values) if y_values else 0
            annotation_y = ymax * 0.95

            # For each known event, compute the group key based on the group_by parameter,
            # then if the event key exists in our grouped data, annotate it.
            for event in known_events:
                event_label = event.get('label', '')
                event_date_str = event.get('date', '')
                try:
                    event_dt = datetime.strptime(event_date_str, '%Y-%m-%d %H:%M:%S')
                except ValueError as ve:
                    print(f"Error parsing event date '{event_date_str}': {ve}")
                    continue

                if group_by == self.GROUP_DAY:
                    event_key = event_dt.strftime('%Y-%m-%d')
                elif group_by == self.GROUP_WEEK:
                    event_key = f"{event_dt.year}-W{event_dt.isocalendar()[1]:02d}"
                elif group_by == self.GROUP_MONTH:
                    event_key = event_dt.strftime('%Y-%m')

                if event_key in key_to_index:
                    x_pos = key_to_index[event_key]
                    # Draw a vertical dashed red line at the event's x position
                    ax.axvline(x=x_pos, color='red', linestyle='--', alpha=0.7)
                    # Place the event label above the bar (or point)
                    ax.text(x_pos, annotation_y, event_label, rotation=90,
                            color='red', fontsize=8, verticalalignment='top', horizontalalignment='center')

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

    # Test 1: Render using the real sample data, grouped by day as a bar chart.
    print("Rendering real sample data grouped by day (Bar Chart):")
    renderer_real = RenderPlot(sample_data)
    renderer_real.render(group_by=RenderPlot.GROUP_DAY, chart_type=RenderPlot.CHART_BAR)

    # Test 2: Render using the fake sample data, grouped by month (Bar Chart).
    print("Rendering fake sample data grouped by month (Bar Chart):")
    renderer_fake = RenderPlot(sample_data_fake)
    renderer_fake.render(group_by=RenderPlot.GROUP_MONTH)

    # Test 3: Render using the fake sample data, grouped by month as a line chart.
    print("Rendering fake sample data grouped by month (Line Chart):")
    renderer_fake_line = RenderPlot(sample_data_fake)
    renderer_fake_line.render(group_by=RenderPlot.GROUP_MONTH, chart_type=RenderPlot.CHART_LINE)
