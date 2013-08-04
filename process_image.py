import Image
import math

class ProcessImage:
    #constructor
    def __init__(self, file_name):
        self.img_file = Image.open(file_name)
        self.img_size = self.img_file.size
        self.width = self.img_size[0]
        self.height = self.img_size[1]
        self.img_bits = self.img_file.bits
        self.img_format = self.img_file.format
        self.mean = [0, 0, 0]
        self.std = [0, 0, 0]

    #get image size
    def getImgSize(self):
        return self.img_size

    #load image
    def loadImg(self):
        self.pixels = self.img_file.load()

    #compute euclidean distance
    def eucDist(self, pix_1, pix_2):
        return math.sqrt(math.pow(pix_1[0] - pix_2[0], 2.0) + math.pow(pix_1[1] - pix_2[1], 2.0) +
                         math.pow(pix_1[2] - pix_2[2], 2.0))

    #compute manhatan distance
    def manDist(self, pix_1, pix_2):
        return (abs(pix_1[0] - pix_2[0]) + abs(pix_1[1] - pix_2[1]) +
                abs(pix_1[2] - pix_2[2]))

    #compute average of samples for a given dimension
    def computeMean(self):
        N = self.width*self.height
        for x in range(self.width):
            for y in range(self.height):
                for index in range(3):
                    self.mean[index] += self.pixels[x, y][index]
        for index in range(3):
            self.mean[index] /= float(N)

    #compute variance
    def computeStdev(self):
        N = self.width*self.height
        for x in range(self.width):
            for y in range(self.height):
                for index in range(3):
                    self.std[index] += math.pow(self.pixels[x, y][index] -
                                           self.mean[index], 2.0)
                
        for index in range(3):
            self.std[index] = math.sqrt(self.std[index]/float(N))

    #check if a pixel is similar
    def checkPixel(self, pixels, width, height, data_tuple):
        for x in range(width):
            for y in range(height):
                if self.manDist(pixels[x, y], data_tuple) <= 2:
                    return True
