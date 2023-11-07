import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms



def get_data_loader(training = True):
    """
    TODO: implement this function.
    INPUT: 
        An optional boolean argument (default value is True for training dataset)

    RETURNS:
        Dataloader for the training set (if training = True) or the test set (if training = False)
    """
    custom_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    #datasets.FashionMNIST()
    train_set = datasets.FashionMNIST('./ data', train = True, download = True, transform = custom_transform)
    test_set = datasets.FashionMNIST('./ data', train = False, transform = custom_transform)
    if training:
        loader = torch.utils.data.DataLoader(train_set, batch_size=64)
    else:
        loader = torch.utils.data.DataLoader(test_set, batch_size=64)
    return loader


def build_model():
        """
        TODO: implement this function.
        INPUT:
            None

        RETURNS:
            An untrained neural network model
        """
        model = nn.Sequential(nn.Flatten(), nn.Linear(28 * 28, 128), nn.ReLU(), nn.Linear(128, 64), nn.ReLU(), nn.Linear(64, 10))
        return model

def train_model(model, train_loader, criterion, T):
    """
    TODO: implement this function.

    INPUT: 
        model - the model produced by the previous function
        train_loader  - the train DataLoader produced by the first function
        criterion   - cross-entropy 
        T - number of epochs for training

    RETURNS:
        None
    """
    #print("model in function ", model)
    #print("train loader in function ", train_loader)
    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    model.train()
    for epoch in range(T):
        running_loss = 0.0
        correct = 0
        total = 0
        #model.train()
        for i, data in enumerate(train_loader, 0):
            # print(i, data)
            # compute using loss function
            # criterion - function, apply this function to outputs and labels and this will give loss
            # after loss, loss.backprop()
            inputs, labels = data
            #print(len(data))
            opt.zero_grad()
            #print(labels)
            outputs = model(inputs)
            #print(outputs)
            #print(outputs)
            loss = criterion(outputs, labels)
            loss.backward()
            opt.step()
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        print("Train Epoch: {}\t Accuracy: {}/{} ({}%) Loss: {} ".format(epoch, correct, total, round(((correct/total) * 100), 2),  round((running_loss / len(train_loader)), 3)))
    


def evaluate_model(model, test_loader, criterion, show_loss = True):
    """
    TODO: implement this function.

    INPUT: 
        model - the the trained model produced by the previous function
        test_loader    - the test DataLoader
        criterion   - cropy-entropy 

    RETURNS:
        None
    """
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    size = 0
    with torch.no_grad():
        for data, labels in test_loader:
            inputs = data
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            size += 1
    if show_loss:
        print("Average loss: {}".format(round((running_loss / size), 4)))
    print("Accuracy: {}%".format(round(((correct/total) * 100), 3)))

def predict_label(model, test_images, index):
    """
    TODO: implement this function.

    INPUT: 
        model - the trained model
        test_images   -  test image set of shape Nx1x28x28
        index   -  specific index  i of the image to be tested: 0 <= i <= N - 1

    RETURNS:
        None
    """
    logits = model(test_images[index])
    prob = F.softmax(logits, dim=1, dtype=float)
    max = prob.data[0][0]
    max_index = 0
    for i in range(len(prob.data[0])):
        if (prob.data[0][i] > max):
            max = prob.data[0][i]
            max_index = i
    max_value = max.item()
    prob.data[0][max_index] = 0
    second_max = prob.data[0][0]
    second_max_index = 0
    for i in range(len(prob.data[0])):
        if (prob.data[0][i] > second_max):
            second_max = prob.data[0][i]
            second_max_index = i
    second_max_value = second_max.item()
    prob.data[0][second_max_index] = 0
    third_max = prob.data[0][0]
    third_max_index = 0
    for i in range(len(prob.data[0])):
        if (prob.data[0][i] > third_max):
            third_max = prob.data[0][i]
            third_max_index = i
    third_max_value = third_max.item()
    class_names = ['T - shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle Boot']
    print("{}: {}%".format(class_names[max_index], round(max_value * 100, 2)))
    print("{}: {}%".format(class_names[second_max_index], round(second_max_value * 100, 2)))
    print("{}: {}%".format(class_names[third_max_index], round(third_max_value * 100, 2)))
    #get the three largest probs


if __name__ == '__main__':
    train_loader = get_data_loader()
    print(type(train_loader))
    print(train_loader.dataset)
    test_loader = get_data_loader(False)
    model = build_model()
    print(model)
    criterion = nn.CrossEntropyLoss()
    train_model(model, train_loader, criterion, 5)
    evaluate_model(model, test_loader, criterion, show_loss=True)
    pred_set, _ = next(iter(test_loader))
    predict_label(model, pred_set, 1)
