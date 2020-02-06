import scipy as sp
import matplotlib.pyplot as plt
import abc
from mpl_toolkits import mplot3d
from sklearn.model_selection import KFold
from scipy.linalg import pinv2

class Classifier:

    def __init__(self, data, comp):
        self.data = data
        self.comp = comp
    
    @abc.abstractmethod
    def train(self, train_index):
        pass

    def set_w(self):
        wh = sp.random.randn(3)
        wd = sp.random.randn(3)
        wa = sp.random.randn(3)
        w0 = sp.random.randn(3)
        self.w = sp.array([wh, wd, wa, w0])
        pass

    def get_x(self, index):
        if self.comp == "b365":
            x = sp.asarray(self.data[index].b365)
        elif self.comp == "bw":
            x = sp.asarray(self.data[index].bw)
        elif self.comp == "iw":
            x = sp.asarray(self.data[index].iw)
        elif self.comp == "lb":
            x = sp.asarray(self.data[index].lb)
        
        x = sp.append(x, 1)
        return sp.transpose(x)  # x = [[x1],[x2],[x3], 1], transpose doen't work on 1xn array
    
    def test(self, test_index):
        correct = 0
        error = 0
        
        for ti in test_index:
            x = self.get_x(ti)
            #  w^T * x
            prediction = (sp.transpose(self.w)).dot(x)
            result = self.data[ti].r
            #  print(f"Prediction: {prediction} \t Result: {result} \t Argmin: {sp.argmin(prediction)} \t Argmax: {sp.argmax(prediction)}")
            if sp.argmax(prediction) == result:
                correct += 1
            else:
                error += 1
        acc = correct/len(test_index)
        #  print(f"Correct: {correct} \t Error: {error} \t Accuracy: {acc}")

        return acc
    
    def start(self):
        kf = KFold(n_splits=10)
        all_accs = 0
        for train_index, test_index in kf.split(self.data):
            self.set_w()
            self.train(train_index)
            all_accs += self.test(test_index)
       
        avg_acc = all_accs/10
        #  print(f"Average Accuracy of Company {self.comp} is: {avg_acc}")
        return avg_acc




class LMS(Classifier):

    def __init__(self, data, comp):
        super(LMS, self).__init__(data, comp)

    def train(self, train_index):
        i = 0
        for ti in train_index:
            x = self.get_x(ti)
            x = sp.reshape(x, (4, 1))
            y = sp.zeros(3) - 1
            y[self.data[ti].r] = 1
            y = sp.reshape(y, (1, 3))
            i += 1
            r = 1 / i 

            #  w(k) = w(k-1) + r * x * (y - x^T * w(k-1))
            temp = self.w + r * x.dot(y - (sp.reshape(x, (1,4)).dot(self.w)))  # transpose doen't work on 1xn array
 
            if sp.any(temp) or sp.any(sp.isneginf(temp)):
                #  print(f"break at {ti} with \nw: {self.w}")
                break
            self.w = temp

class MS(Classifier):

    def __init__(self, data, comp):
        super(MS, self).__init__(data, comp)

    def get_y(self, index):
        y = sp.zeros(3) - 1
        y[self.data[index].r] = 1
        return y
        

    def train(self, train_index):
        x = sp.array([self.get_x(i) for i in train_index])
        y = sp.array([self.get_y(i) for i in train_index])

        #  w = x^+ * y
        self.w = pinv2(x, check_finite=True).dot(y)

        
        
    

