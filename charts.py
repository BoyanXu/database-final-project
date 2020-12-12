from pychartjs import BaseChart, ChartType, Color

class MyBarGraph(BaseChart):

    type = ChartType.Bar

    class data:
        label = "Numbers"
        data = [12, 19, 3, 17, 10]
        backgroundColor = Color.Green

class SpendingChart(BaseChart):
    type = ChartType.Bar
    class data:
        class spendings:
            data = [20, 30, 40, 20, 30, 10, 20, 10, 10, 0, 0, 0]
            backgroundColor = Color.Green