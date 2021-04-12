import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
SEED =12
def load_labels(label_file):
    """Loads image filenames, classes, and bounding boxes"""
    fnames, classes, bboxes = [], [], []
    with open(label_file, 'r') as f:
        for line in f.readlines():
            fname, cls, xmin, ymin, xmax, ymax = line.strip('\n').split()
            fnames.append(fname)
            classes.append(int(cls))
            bboxes.append((int(xmin), int(ymin), int(xmax), int(ymax)))
    fnames = ["C:\project\data\\2A_images\\" + fname for fname in fnames]
    fnames = np.array(fnames)
    classes = np.array(classes)
    return fnames, classes, bboxes
def index_generator(fnames , SET):
    """Genrated random index of a particular class"""
    np.random.seed(SEED)
    index = np.random.randint(1,len(fnames),size = SET)
    return index 
def numberofclasses(classes, index):
    class0 = len((np.where(classes[index]==0))[0])
    class1 = len((np.where(classes[index]==1))[0])
    class2 = len((np.where(classes[index]==2))[0])
    return class0  , class1, class2
def dataframe_generator(test_index ,classes_test ):
    """Returns 1 dataframes of datasets distribution"""
    index = ["Normal" , "Pneumonia" , "COIVD -19"]
    test_DF = numberofclasses(classes_test, test_index)
    df = pd.DataFrame({'test': test_DF } , index = index)
    return df
def data_constructor(filepath, classes , dim_size ,index  ,bboxes , interpolation = cv2.INTER_AREA , intensify =False):
    """Constructs and splits X and Y for training , validtion and test"""
    np.random.seed(SEED)
    y = np.array(classes[index])
    x = []
    for i in index:
        img  = cv2.imread(filepath[i])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        x1,y1,x2,y2 = bboxes[i]
        img = img[y1:y2,x1:x2]
        img = cv2.resize(img, dim_size , interpolation = interpolation)
        x.append(img)
    
    x = np.array(x)
    if intensify == True:
        x= x/255
    return x , y 
def phase1_labels_updater(dense_y):
    """
    Updates labels for Phase-1 testing
    """
    for i in range(len(dense_y)):
        if dense_y[i] == 2:
            dense_y[i] =1 
        elif dense_y[i]==1:
            dense_y[i] = 0 
    return dense_y    
def index_extractor(y_preds, y_test,  test_index ,classes_test):
    """
    Extracts indexs of all the Original classes and Predicted classes by Phase-1 Model 
    """
    yclass_0 = np.where(y_preds==0)[0]
    yclass_1 = np.where(y_preds==1)[0]
    class_0 = np.where(y_test==0)[0]
    class_1 = np.where(y_test==1)[0]
    yclass0 = test_index[yclass_0]
    yclass1 = test_index[yclass_1]
    class0 = test_index[class_0]
    class1 =test_index[class_1]
    y00=np.where(classes_test[yclass0]==0)[0]
    y01=np.where(classes_test[yclass0]==1)[0]
    y02=np.where(classes_test[yclass0]==2)[0]
    y20=np.where(classes_test[yclass1]==0)[0]
    y21=np.where(classes_test[yclass1]==1)[0]
    index_00 = yclass0[y00]
    index_01 = yclass0[y01]
    index_02 = yclass0[y02]
    index_20 = yclass1[y20]
    index_21 = yclass1[y21]
    index_0 = np.concatenate((index_00,index_01))
    return index_0,index_02,index_20,index_21
def plot_confusion_matrix(cm, classes,normalize=False,title='Confusion matrix',cmap=plt.cm.Blues):
    """
      This function prints and plots the confusion matrix.
    """
    print(cm)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt), horizontalalignment="center",color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()
