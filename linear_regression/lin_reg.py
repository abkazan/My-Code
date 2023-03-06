import sys
import csv
from matplotlib import pyplot as plt
import numpy as np


def q2(X, Y):
    plt.plot(np.asarray(X, float), Y)
    # pri
    plt.xlabel("Year")
    plt.ylabel("Number of Frozen Days")
    # print("xticks ", plt.xticks())
    # print(np.divide())
    # plt.xticks(np.array(X) / )
    plt.savefig("plot.jpg")


def q2_and_q3(file):
    X = []
    q2_x = []
    Y = []
    for line in file.readlines():
        if (line[0].isdigit()):
            xi = line[0:4]
            yi = line[5:]
            feature_vector = [int(1), int(xi)]
            Y.append(int(yi))
            X.append(feature_vector)
            q2_x.append(xi)
    # print(np.asmatrix(X))
    # Q2
    q2(q2_x, Y)
    X = np.asmatrix(X)
    Y = np.asarray(Y)
    Z = np.dot(X.T, X)
    print("Q3a:")
    print(X)
    print("Q3b:")
    print(Y)
    print("Q3c:")
    print(Z)
    I = np.linalg.inv(Z)
    print("Q3d:")
    print(I)
    PI = np.dot(I, X.T)
    print("Q3e:")
    print(PI)
    hat_beta = np.squeeze(np.asarray(np.dot(PI, Y)))
    # hat_beta = np.squeeze(np.asarray(hat_beta))
    print("Q3f:")
    print(hat_beta)
    return hat_beta


def q4(hat_beta, x_test):
    # print(hat_beta[1])
    y_test = hat_beta[0] + (hat_beta[1] * x_test)
    print("Q4: " + str(y_test))


def q5(hat_beta):
    symbol = ""
    explanation = ""
    if hat_beta[1] < 0:
        symbol = "<"
        # print("negative")
        explanation = "This means that the number of frozen days predicted for 2021-2022 will decrease based on the trajectory of the previous years"
    if hat_beta[1] > 0:
        symbol = ">"
        explanation = "This means that the number of frozen days predicted for 2021-2022 will decrease based on the trajectory of the previous years"
        # print("positive")
    if hat_beta[1] == 0:
        symbol = "="
        explanation = "This means that the number of frozen days predicted for 2021-2022 will stay roughly the same based on the trajectory of the previous years"
        # print("zero" + symbol)
    print("Q5a: " + symbol)
    print("Q5b: " + explanation)
    # include explanation for q5b


def q6(hat_beta):
    # print(hat_beta[0] + hat_beta[1])
    x = (-hat_beta[0]) / hat_beta[1]
    explanation = ""
    print("Q6a: " + str(x))
    if (x > 2100):
        explanation += "This could be a compelling prediction, however, it is in the distant future and only considers the previous trajectory of the data. " \
                       "It does not take into account the possible increase of global warming and possible natural disasters that could occur in the future"
    if (x < 2100 and x > 2021):
        explanation += "This means that Lake Mendota will either stop freezing completely in the near future, or have very little frozen days. " \
                       "This could be realistic, however, the previous data shows that Lake Mendota is still frozen for over 50 days in recent years, with the exception of 2001." \
                       "While the data has steadily decreased in the 21st century, it should still be a while before Lake Mendota stops freezing completely"
    if (x < 2021):
        explanation += "This is not likely. This means that Lake Mendota has already been frozen for zero days, which according to the dataset, it hasn't. " \
                       "Either the data, or the code is wrong"
    print("Q6b: " + explanation)


def main():
    # print(sys.argv)
    # print("hello world")
    # q1: data curatiom
    """
    f = open('hw5.csv', 'w')
    days = open('days.txt', 'r')
    years = open('years.txt', 'r')
    writer = csv.writer(f)
    heading = ['year', 'days']
    writer.writerow(heading)
    for (year_line, day_line) in zip(years.readlines(), days.readlines()):
        line = [year_line.strip()[0:4], day_line.strip()]
        writer.writerow(line)
    """
    # print(sys.argv[1])
    f = open(sys.argv[1], 'r')
    hat_beta = q2_and_q3(f)
    q4(hat_beta, 2021)
    # print(len(f.readlines()))
    # X = np.empty([len(f.readlines()), 2])
    q5(hat_beta)
    q6(hat_beta)
    # np.append(X, [0,1])

if __name__ == '__main__':
    main()
