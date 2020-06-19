import coderec_sqlpart
import matplotlib.pyplot as plt


def visualize():
    list_tuples=coderec_sqlpart.get_list_of_data()
    xaxis=[t[0] for t in list_tuples]
    yaxis=[t[1] for t in list_tuples]  
    plt.xlabel('Date')
    plt.ylabel('No of problems solved')
    plt.plot(xaxis, yaxis, color='green', linestyle='dashed', linewidth = 3, marker='o', markerfacecolor='blue', markersize=12)
    plt.show()


visualize()