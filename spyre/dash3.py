from spyre import server
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import pandas as pd

class StockExample(server.App):

    def __init__(self):
        df = pd.read_csv("filename_createdate.csv")
        df.loc[:, "CONTENTCREATEDDATE"] = pd.to_datetime(df.CONTENTCREATEDDATE)
        df_date = df.groupby("CONTENTCREATEDDATE").count()[8:] #Ignore the migration
        self.data = df_date

    title = "Total Docs"

    controls = [{   "type" : "hidden",
                    "id" : "update_data"}]

    outputs = [{ "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    }]

    def getData(self, params):
        year = params['year']
        plot_type = params['plot_type']
        data = self.data

        if plot_type == 'month':
            index = data.index.month
        else:
            index = data.index.dayofweek

        data = pd.pivot_table(data, index=index, columns=data.index.year,
                                values='TITLE', aggfunc='sum')
        if year == 'all':
            return data
        else:
            return data[int(year)]

    def getPlot(self, params):
        df = self.getData(params)
        plt_obj = df.plot(title="Files uploaded on year {}".format(str(params['year'])))
        plt_obj.set_ylabel("Files Uploaded")
        plt_obj.set_xlabel("Doc Upload Date")
        plt_obj.set_title(params['year'])
        fig = plt_obj.get_figure()
        return fig

if __name__ == '__main__':
    app = StockExample()
    years = pd.unique(app.data.index.year)
    options = [{"label": "all", "value":"all"}]
    opt_ext = [{"label": str(x), "value":x} for x in years.tolist()]
    options.extend(opt_ext)
    app.inputs = [{ "type":'dropdown',
                    "label": 'Year',
                    "options" : options,
                    "key": 'year',
                    "action_id": "update_data"},
                    {"type":'radiobuttons',
        			"label": 'Choose',
        			"options" : [
        				{"label": "by Month", "value":"month", "checked":True},
        				{"label":"by Days of the Week", "value":"day"}
        			],
        			"key": 'plot_type',
        			"action_id" : "update_data",
        			},
                    ]
    app.launch(port=9093)
