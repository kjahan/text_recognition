from process_image import ProcessImage
import math

class Train():
    def __init__(self, num):
        self.samples = []
        self.num = num
        self.tot_mean = [0.0, 0.0, 0.0]
        self.tot_std = [0.0, 0.0, 0.0]
        #lets' go through all sample inputs and extract their distributions
        for i in range(1, num + 1):
            sample_file = "buses/sample_" + str(i) + ".jpg"
            #sample_file = "../buses/boundary.jpg"
            sample = ProcessImage(sample_file)
            print "train image size:"
            print sample.getImgSize()
            #load training data for bus head sign
            sample.loadImg()
            self.samples.append(sample)
        self.computeTotMean()
        self.computeTotStd()

    #print sample values
    def printSample(self, sample):
        for x in range(sample.width):
            for y in range(sample.height):
                print "(%d, %d, %d)" % (sample.pixels[x,y][0],
                                    sample.pixels[x,y][1], sample.pixels[x,y][2])
    #get sample mean
    def getSampleMean(self, sample):
        sample.computeMean()
        print "sample mean=(%f, %f, %f)" % (sample.mean[0], sample.mean[1],
                                        sample.mean[2])

    #get sample std
    def getSampleStd(self, sample):
        sample.computeStdev()
        print "stdev=(%f, %f, %f)" % (sample.std[0], sample.std[1],
                                        sample.std[2])

    #compute total mean
    def computeTotMean(self):
        #lets' go through all sample inputs and extract their means
        for sample in self.samples:
            self.getSampleMean(sample)
            self.tot_mean[0] += sample.mean[0]
            self.tot_mean[1] += sample.mean[1]
            self.tot_mean[2] += sample.mean[2]

        self.tot_mean = [item/float(self.num) for item in self.tot_mean]

    #compute total std
    def computeTotStd(self):
        #lets' go through all sample inputs and extract their stds
        tot_N = 0
        for sample in self.samples:
            self.getSampleStd(sample)
            N = sample.width*sample.height
            tot_N += N
            for x in range(sample.width):
                for y in range(sample.height):
                    for index in range(3):
                        self.tot_std[index] += math.pow(sample.pixels[x, y][index] -
                                           self.tot_mean[index], 2.0)
                
        for index in range(3):
            self.tot_std[index] = math.sqrt(self.tot_std[index]/float(tot_N))

