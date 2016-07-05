plot_conf = {
    ########################
    #      Data config     #
    ########################
    "x": "epoch",       # x axis data
    "y": ["test_acc"],  # y axis data, multiple items are allowed
    "score": "acc",     # convert y data to acc, err
    "scale": 100,       # scale data in this range
    "y_min": 'auto',         # min y to display
    "y_max": 'auto',       # max y to display
    ########################
    #      GUI CONFIG      #
    ########################
    "legend": True,     # show legend
    "xlabel": "",
    "ylabel": "",
}