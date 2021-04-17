import cv2
import numpy as np
import pandas as pd
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
def dataframe_generator(train_index , valid_index , classes_train , classes_valid ):
    """Returns 1 dataframes of datasets distribution"""
    index = ["Normal" , "Pneumonia" , "COIVD -19"]
    train_DF = numberofclasses(classes_train, train_index)
    valid_DF = numberofclasses(classes_valid, valid_index)
    df = pd.DataFrame({'train': train_DF ,'valid' : valid_DF} , index = index)
    return df
def train_index_updater(classes_train , train_index,n ):
    """Updates train_index for class balance"""
    np.random.seed(SEED)
    class0_train = np.where(classes_train[train_index]==0)[0]
    class1_train = np.where(classes_train[train_index]==1)[0]
    class2_train = np.where(classes_train[train_index]==2)[0]
    class0 =train_index[class0_train]
    class1 = train_index[class1_train]
    np.random.seed(SEED)
    class22 = np.random.choice(class2_train , n)
    class2 = train_index[class22]
    train_index_updated = np.concatenate((class0 , class1 , class2))
    np.random.shuffle(train_index_updated)
    return train_index_updated

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