import pandas as pd
import matplotlib.pyplot as plt


def print_scores(label, scores):
    print(f"{label} Score Time: %.2f" % (scores['score_time'].mean() * 100))
    print(f"{label} Test Accuracy: %.2f%%" % (scores['test_accuracy'].mean() * 100))
    print(f"{label} Train Accuracy: %.2f%%" % (scores['train_accuracy'].mean() * 100))
    print(f"{label} Test Precision Weighted Accuracy: %.2f%%" % (scores['test_precision_weighted'].mean() * 100))
    print(f"{label} Train Precision Weighted Accuracy: %.2f%%" % (scores['train_precision_weighted'].mean() * 100))
    print(f"{label} Test Recall Weighted Accuracy: %.2f%%" % (scores['test_recall_weighted'].mean() * 100))
    print(f"{label} Train Recall Weighted Accuracy: %.2f%%" % (scores['train_recall_weighted'].mean() * 100))
    print(f"{label} Test F1 Accuracy: %.2f%%" % (scores['test_f1_weighted'].mean() * 100))
    print(f"{label} Train F1 Accuracy: %.2f%%\n" % (scores['train_f1_weighted'].mean() * 100))


def readTemperatures(csv_file):
    with open(csv_file) as file:
        file.readline()
        csv_file = csv.reader(file)
        time = []
        temperature = []
        for row in csv_file:
            e = row[0].split()
            time.append(e[0])
            temperature.append(e[1])

        return time, temperature


def plotTimeTemperature(path):
    df = pd.read_csv(path, delimiter="\t")
    df = pd.DataFrame(df)
    time_data = df[df.columns[0]]
    temperature_data = df[df.columns[1]]
    plt.plot(time_data, temperature_data)
    plt.xlabel("Time")
    plt.ylabel("Temperature")
    plt.title("Thermode temperature over time diagram")
    plt.show()

