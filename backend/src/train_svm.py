from modules.SVM import SVM, SVM_DataLoader
from utils import getSubFilePaths

def main():
    model_path = "./src/data/svm.pth"

    loader = SVM_DataLoader()
    svm = SVM(model_path)

    for i, region in enumerate(["hyogo", "kyoto", "osaka"]):
        for path in getSubFilePaths("./src/assets/tensor/" + region):
            loader.load_vectors(path, i)
    
    svm.train(loader)
    svm.save(model_path)

if __name__ == "__main__":
    main()