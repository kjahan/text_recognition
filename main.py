from train import Train
from classify import Classify
import sys

def main(test_file, threshold):
    #extract pdfs
    train = Train(1)
    #print train.tot_mean
    #print train.tot_std
    #compute probability for test data
    ai = Classify(test_file, train, threshold)
    return 0

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('Usage: %s test-file threshod' % sys.argv[0])
    main(sys.argv[1], float(sys.argv[2]))
