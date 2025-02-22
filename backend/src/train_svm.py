from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

import numpy as np
import torch

from utils import getSubFilePaths

def load_dataset() -> tuple[np.ndarray, np.ndarray]:
    regions = []
    labels = []
    for i, region in enumerate(["hyogo", "kyoto", "osaka"]):
        arrays = []
        for path in getSubFilePaths("./src/assets/tensor/" + region):
            arr = torch.load(path).detach().cpu().numpy()
            arr = arr.reshape(-1, arr.shape[-1])
            arrays.append(arr)

        array = np.concat(arrays, axis=0)
        regions.append(array)
        labels.append(np.ones(array.shape[0]) * i)

    data = np.concat(regions, axis=0)
    labels = np.concat(labels, axis=0)
    print(data.shape, labels.shape)

    return data, labels

def main():    
    train_x, test_x, train_y, test_y = train_test_split(*load_dataset(), test_size=0.1)
    print(train_x.shape, test_x.shape, train_y.shape, test_y.shape)

    for data_nums in [5000, 10000, 20000, 50000]:
        last_acc = 0
        for i in range(10):
            inds = np.random.randint(0, train_x.shape[0], (data_nums))
            x = train_x[inds]
            y = train_y[inds]

            model = svm.LinearSVC(C=0.1 + i/3)
            model.fit(x, y)

            output = model.predict(test_x)
            acc = accuracy_score(test_y, output)
            print("accuracy:", acc)

            if acc > last_acc:
                last_acc = acc

                weight = torch.tensor(model.coef_, dtype=torch.float32)
                bias = torch.tensor(model.intercept_, dtype=torch.float32)

                linear = torch.nn.Linear(768, 3, bias=True)
                with torch.no_grad():
                    linear.weight.copy_(weight)
                    linear.bias.copy_(bias)

                torch.save(linear, "./src/data/svm_linear_" + str(data_nums) + ".pth")
                print("saved!")

if __name__ == "__main__":
    main()