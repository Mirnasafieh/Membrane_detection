import seaborn as sns
import matplotlib.pyplot as plt

from data_handeling import data_import



def barplot_E3E4(data,parameterx, parametery):
    """ This function creates a bar graph according to the parameters given"""
    graph=sns.barplot(x=parameterx, y=parametery, palette="Greens",  data=data).set_title("Receptor IOD")
    return graph

def all_compartments_lines(data):
    """This function creates a line graph of both genottypes in all the compartments for given receptor"""
    graph=sns.catplot(x="compartment", y="M1", hue="cell genotype",
        palette="Greens",
        markers=["^", "o"], linestyles=["--","--"],
        kind="point", data=data)

    return graph 

def all_compartments_bars(data):
    """This function creates a barplot map of both genottypes in all the compartments for given receptor"""    
    g = sns.FacetGrid(data, col="compartment", height=4, aspect=.5)
    result= g.map(sns.barplot, "cell genotype", "M1", palette='Greens')
    return result

def save_graph(graph, file_name, parameter):
    saving_name= file_name.split()[0]
    plt.savefig(saving_name+ parameter +".pdf")

if __name__ == "__main__":
    df=data_import("ApoER2 colocalization.xlsx")
    sns.set(style="whitegrid")



    plt.show()