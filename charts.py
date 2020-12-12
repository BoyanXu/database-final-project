from pychartjs import BaseChart, ChartType, Color

class MyBarGraph(BaseChart):

    type = ChartType.Bar

    class data:
        label = "Numbers"
        data = [12, 19, 3, 17, 10]
        backgroundColor = Color.Green

# class SpendingChart(BaseChart):
#     type = ChartType.Bar

#     class label:

#     class data:
#         label = "Numbers"
#         data = [12, 19, 3, 17, 10]
#         backgroundColor = Color.Green