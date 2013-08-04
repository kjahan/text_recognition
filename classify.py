from process_image import ProcessImage

class Classify:
    def __init__(self, test_file, train, threshold):
        self.test_file = test_file
        #compute probability for test data
        self.test = ProcessImage(self.test_file)
        self.test.loadImg()
        print "test image size:"
        print self.test.getImgSize()
        self.N = self.test.width*self.test.height
        self.train = train
        self.gauss_threshold = threshold
        self.lower_bound = 1.0/3.0
        self.upper_bound = 2.0/3.0
        self.extractLetters()

    def extractLetters(self):
        self.runGaussian()

    def runGaussian(self):
        passed = 0
        #threshold = 1.0
        self.letter = []
        for x in range(self.test.width):
            for y in range(self.test.height):
                z1 = abs(self.test.pixels[x,y][0] - self.train.tot_mean[0])/self.train.tot_std[0]
                z2 = abs(self.test.pixels[x,y][1] - self.train.tot_mean[1])/self.train.tot_std[1]
                z3 = abs(self.test.pixels[x,y][2] - self.train.tot_mean[2])/self.train.tot_std[2]
                #print "-----> (z1=%f, z2=%f, z3=%f)" % (z1, z2, z3)
                #print "(r=%f, g=%f, b=%f)" % (test.pixels[x,y][0],
#                                          test.pixels[x,y][1],
 #                                         test.pixels[x,y][2])
                if (z1 <= self.gauss_threshold) and (z2 <= self.gauss_threshold) and (z3 <= self.gauss_threshold):
                    passed += 1
                    #print "(x=%d, y=%d)" % (x, y)
                    #print "(z1=%f, z2=%f, z3=%f)" % (z1, z2, z3)
                    self.letter.append((x,y))
        self.extractXYMaps()
        self.extractVertHorizLines()
        self.detectLeftMost()
        self.detectRightMost()
        self.detectBottomHorizLine()
        self.detectTopHorizLine()
        self.printDetectedLines()

    def extractXYMaps(self):
        #store x map
        self.x_map = {}
        for point in self.letter:
            if point[0] not in self.x_map:
                self.x_map[point[0]] = [point[1]]
            else:
                self.x_map[point[0]].append(point[1])
        #store y map
        self.y_map = {}
        for point in self.letter:
            if point[1] not in self.y_map:
                self.y_map[point[1]] = [point[0]]
            else:
                self.y_map[point[1]].append(point[0])

    def extractVertHorizLines(self):
        #detect vertical lines
        self.vertical = {}
        for key, value in self.x_map.iteritems():
            vertical_len = value[-1] - value[0]
            value.sort()
            #find gap
            max_gap = 0
            for index in range(len(value) - 1):
                if abs(value[index] - value[index+1]) > max_gap:
                    max_gap = abs(value[index] - value[index+1])
            self.vertical[key] = (len(value), max_gap, vertical_len)
        
        #detect horizontal line
        self.horizontal = {}
        for key, value in self.y_map.iteritems():
            horizontal_len = value[-1] - value[0]
            value.sort()
            #find gap
            max_gap = 0
            for index in range(len(value) - 1):
                if abs(value[index] - value[index+1]) > max_gap:
                    max_gap = abs(value[index] - value[index+1])
            self.horizontal[key] = (len(value), max_gap, horizontal_len)
 
    def detectLeftMost(self):
        #find leftmost
        self.max_l_line = 0
        self.max_l_x = 0
        for x in range(int(self.test.width*self.lower_bound)):
            if x in self.vertical and self.vertical[x][0] > self.max_l_line:
                self.max_l_line = self.vertical[x][0]
                self.max_l_x = x
    
    def detectRightMost(self):
        #find rightmost
        self.max_r_line = 0
        self.max_r_x = 0
        for x in range(int(self.test.width*self.upper_bound), self.test.width):
            if x in self.vertical and self.vertical[x][0] > self.max_r_line:
                self.max_r_line = self.vertical[x][0]
                self.max_r_x = x
    
    def detectBottomHorizLine(self):
        #find bottom horizontal line
        self.max_b_line = 0
        self.max_b_y = 0
        gap = 0
        for y in range(int(self.test.height*self.upper_bound), self.test.height):
            if y in self.horizontal and self.horizontal[y][0] > self.max_b_line:
                self.max_b_line = self.horizontal[y][0]
                gap = self.horizontal[y][1]
                self.max_b_y = y
    
    def detectTopHorizLine(self):
        #find top horizontal line
        self.max_t_line = 0
        self.max_t_y = 0
        for y in range(int(self.test.height*self.lower_bound)):
            if y in self.horizontal and self.horizontal[y][0] > self.max_t_line:
                self.max_t_line = self.horizontal[y][0]
                self.max_t_y = y
    
    def printDetectedLines(self):
        print "detected patterns:"
        print "left-most-line: x=%d & len=%d" % (self.max_l_x, self.max_l_line)
        print "right-most-line: x=%d & len=%d" % (self.max_r_x, self.max_r_line)
        print "bottom-line: y=%d & len=%d" % (self.max_b_y, self.max_b_line)
        print "top-line: y=%d & len=%d" % (self.max_t_y, self.max_t_line)
        #print "total=%d" % self.N
        #print "passed=%d" % self.passed
