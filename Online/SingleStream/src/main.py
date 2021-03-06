#!/usr/bin/env python3
import torch
import torch.nn as nn
from dataloader import get_loaders
from model import SingleStream
from train import train_network
import sys
sys.path.insert(0, 'utils')
from plotting import plot_data

def main():
    """Main Function."""
    # dataloader parameters
    gpu = torch.cuda.is_available()
    train_path = 'data/train_data.txt'
    valid_path = 'data/valid_data.txt'
    batch_size = 2
    sequence_len = 50
    window_size = 5
    flow = False
    num_workers = 2
    # network parameters
    model = 'VGGNet19'
    rnn_hidden = 512
    rnn_layers = 1
    # training parameters
    max_epochs = 1
    learning_rate = 1e-4
    criterion = nn.CrossEntropyLoss()

    # get loaders
    dataloaders, dataset_sizes = get_loaders(train_path, valid_path, batch_size,
            sequence_len, window_size, flow, num_workers, gpu)

    # create network and optimizer
    net = SingleStream(model, rnn_hidden, rnn_layers, pretrained=True)
    print(net)
    optimizer = torch.optim.Adam(net.parameters(), learning_rate)
    # train the network
    net, val_acc, losses, accuracies = train_network(net, dataloaders, 
            dataset_sizes, batch_size, sequence_len, window_size, criterion, 
            optimizer, max_epochs, gpu)
    # plot
    if flow:
        s_plots = 'outputs/online/SingleStreamFlowPlots.png'
        s_params = 'outputs/online/SingleStreamFlowParams.pkl'
    else:
        s_plots = 'outputs/online/SingleStreamAppPlots.png'
        s_params = 'outputs/online/SingleStreamAppParams.pkl'

    # plot
    plot_data(losses, accuracies, s_plots)
    # save network
    torch.save(net.state_dict(), s_params)


if __name__ == '__main__':
    main()
