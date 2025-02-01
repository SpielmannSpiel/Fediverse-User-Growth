import matplotlib.pyplot as plt


class RenderPlot:
    def __init__(self, data):
        """
        Initialize the renderer with the data.

        Parameters:
            data (list): A list of dictionaries, where each dictionary has
                         keys 'id', 'total_users', and 'date_checked'.
        """
        self.data = data

    def render(self):
        """
        Render a bar chart using Matplotlib in XKCD style.
        """
        # Extract the x and y values from the data
        x_values = [item['id'] for item in self.data]
        y_values = [item['total_users'] for item in self.data]

        # Apply the XKCD style
        with plt.xkcd():
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(x_values, y_values, color='skyblue')

            # Set chart title and labels
            ax.set_title('Monthly Stats: Total Users per ID')
            ax.set_xlabel('ID')
            ax.set_ylabel('Total Users')

            # Optionally, adjust ticks if the data is too cluttered
            ax.set_xticks(x_values)
            plt.xticks(rotation=45)

            plt.tight_layout()
            plt.show()