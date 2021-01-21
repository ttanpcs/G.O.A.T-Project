import numpy as np
import random
import cv2

def resizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def standardizeImage(file_path):
    return resizeWithAspectRatio(cv2.imread(file_path), width = 500)

class GoModel:
    def __init__(self, size, background = None):
        black_cascade_file = "./resources/blackCascade.xml"
        white_cascade_file = "./resources/whiteCascade.xml"
        empty_cascade_file = "./resources/emptyCascade.xml"
        self.empty_cascade = cv2.CascadeClassifier(empty_cascade_file)
        self.black_cascade = cv2.CascadeClassifier(white_cascade_file)
        self.white_cascade = cv2.CascadeClassifier(black_cascade_file)
        self.size = size
        self.last_board_image = background
        self.last_board_array = np.zeros((self.size, self.size), dtype = int)

    def createBoard(self, centers, corners, output): # (This Method should be abstracted to work when using Image differencing. ie: finds the new one and places it, ignores old/removed.)
        if corners is not None and len(corners) > 3: # (Do Later, should be used for hand detection or smth)
            flat_corners = np.array([[0, 0],
                                    [self.size - 1, 0],
                                    [self.size - 1, self.size - 1],
                                    [0, self.size - 1]],
                                dtype="float32")
            persp = cv2.getPerspectiveTransform(corners, flat_corners)
            types = ["black_rectangles", "white_rectangles"]
            numerical_values = {"black_rectangles": 1, "white_rectangles": 2}
            for stone in types:
                if len(centers[stone]) > 0:
                    stones = np.array(centers[stone], dtype="float32")
                    stones = np.array([stones])
                    stones_flat = cv2.perspectiveTransform(stones, persp)
                    for i in stones_flat[0]:
                        x = int(round(i[0]))
                        y = int(round(i[1]))
                        if x >= 0 and x < self.size and y >= 0 and y < self.size:
                            output[x][y] = numerical_values[stone]

    def sortPoints(self, box):
        rect = np.zeros((4, 2), dtype = "float32")

        s = box.sum(axis = 1)
        rect[0] = box[np.argmin(s)]
        rect[2] = box[np.argmax(s)]

        diff = np.diff(box, axis = 1)
        rect[1] = box[np.argmin(diff)]
        rect[3] = box[np.argmax(diff)]

        return rect

    def fourCorners(self, hull, dimensions): # (Figure out what this method does)
        length = len(hull)

        if length < 4:
            return []
        
        allLines = []
        for i in range(length):
            if i == (length - 1):
                line = [[hull[i][0][0], hull[i][0][1]], [hull[0][0][0], hull[0][0][1]]]
            else:
                line = [[hull[i][0][0], hull[i][0][1]], [hull[i + 1][0][0], hull[i + 1][0][1]]]
            d = np.sqrt((line[0][0] - line[1][0])**2 + (line[0][1] - line[1][1])**2)
            allLines.append([line, d])

        allLines.sort(key=lambda x: x[1], reverse=True)
        lines = []
        for i in range(4):
            lines.append(allLines[i][0])

        equations = []
        for i in lines:
            x_coords, y_coords = zip(*i)
            A = np.vstack([x_coords, np.ones(len(x_coords))]).T
            m, c = np.linalg.lstsq(A, y_coords)[0]
            equations.append([m, c])

        intersections = []
        for i in equations:
            for j in equations:
                if i[0] == j[0]:
                    pass
                else:
                    a = np.array([[i[0] * -1, 1], [j[0] * -1, 1]])
                    b = np.array([i[1], j[1]])
                    solution = np.linalg.solve(a, b)
                    if solution[0] > 0 and solution[1] > 0 and solution[0] < dimensions[0] and solution[1] < dimensions[1]:
                        intersections.append([solution[0], solution[1]])

        intersections.sort()
        
        if len(intersections) > 6:
            output = [intersections[0],
                    intersections[2],
                    intersections[4],
                    intersections[6]]
            box = self.sortPoints(np.array(output, dtype="float32"))
            return box
        else:
            return []

    def findGroupMembers(self, maxDistance, i, distances, group):
        for j in range(len(group)):
            if group[j]:
                pass
            elif distances[i][j] < maxDistance:
                group[j] = True
                self.findGroupMembers(maxDistance, j, distances, group)

    def findGroup(self, spots):
        length = len(spots)
        distances = np.zeros((length, length), dtype="float32")
        distanceList = []
        
        for i in range(length):
            for j in range(length):
                distance = np.sqrt((spots[i][0] - spots[j][0])**2 + (spots[i][1] - spots[j][1])**2)
                distances[i][j] = distance
                if distance > 0:
                    distanceList.append(distance)
        distanceList.sort()
        numDistances = int((self.size - 1)**2 * 1.8) # (Doesn't Seem Right -TT) number of distances that should be between spots on a board
        maxDistance = np.mean(distanceList[0:numDistances]) * 1.75 # (Huh) a little bigger than that, for luck
        minGroup = int(self.size**2 * 0.75) # (Change this number later if necessary)
        group = np.zeros((length), dtype="bool_")

        for i in range(length):
            self.findGroupMembers(maxDistance, i, distances, group)
            if group.sum() >= minGroup:
                outPoints = []
                for k in range(length):
                    if group[k]:
                        outPoints.append(spots[k])
                return outPoints
            else:
                group = np.zeros((length), dtype="bool_")

    def findCenters(self, image):
        rectangles = dict()
        centers = dict()
        rectangles["white_rectangles"] = self.white_cascade.detectMultiScale(image, 1.1, 1)
        rectangles["black_rectangles"] = self.black_cascade.detectMultiScale(image, 1.1, 1)
        rectangles["empty_rectangles"] = self.empty_cascade.detectMultiScale(image, 1.08, 1)

        centers["white_rectangles"] = []
        centers["black_rectangles"] = []
        centers["empty_rectangles"] = []
        for key in rectangles:
            for (ex, wy, w, h) in rectangles[key]:
                x = ex + w / 2.0
                y = wy + w / 2.0
                centers[key].append([x, y])

        return centers

    def findCorners(self, centers, dimensions):
        group = self.findGroup(centers["white_rectangles"] + centers["black_rectangles"] + centers["empty_rectangles"])
        if group is None:
            return None
        hull = cv2.convexHull(np.array(group, dtype="int32"))
        epsilon = 0.001*cv2.arcLength(hull, True)
        approx = cv2.approxPolyDP(hull, epsilon, True)
        
        return self.fourCorners(approx, dimensions)        

    def findCriticalPoints(self, image):
        centers = self.findCenters(image)
        (h, w, d) = image.shape
        dimensions = (w, h)
        corners = self.findCorners(centers, dimensions)
        return centers, corners

    def readBoard(self, image):
        output = np.zeros((self.size, self.size), dtype = int)
        centers, corners = self.findCriticalPoints(image)
        self.createBoard(centers, corners, output)
        return output

    def showBoard(self, image):
        centers = self.findCenters(image)
        for key in centers:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            for c in centers[key]:
                cv2.circle(image,
                            (int(round(c[0])), int(round(c[1]))),
                            3,
                            (r, g, b),
                            -1)
        cv2.imshow('Board', image)
        cv2.waitKey()

    def readBoard(self, image, is_black_turn):
        output = np.zeros((self.size, self.size), dtype = int)
        centers, corners = self.findCriticalPoints(image)
        cascade_output = self.createBoard(centers, corners, output)

        if (self.last_board_image != None):
            last_gray = cv2.GaussianBlur(cv2.cvtColor(self.last_board_image, cv2.COLOR_BGR2GRAY), (5, 5), 0)
            current_gray =  cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (5, 5), 0)
            difference = cv2.threshold(cv2.absdiff(last_gray, current_gray), 25, 255, cv2.THRESH_BINARY)
            detector = cv2.SimpleBlobDetector()
            keypoints = detector.detect(difference) # https://www.javatpoint.com/opencv-blob-detection
            
            # test_image = cv2.drawKeypoints((image, keypoints, np.array([])), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  # Test This Line
)

            # Call subtraction of image - self.last_board_image -> then do blob detection and find centers.
                    # Need some way to deal with floating hands or smth??? maybe using the black and white classifiers here might work? 
                    # If hand then quit and return something
                    # Idea 1: use blob detection and if not all blobs are similar size. think 1.1x? then quit 
            # Figure out the color of that placed tile? (Maybe try using the cascade clasifiers on the board) ie go through and place all the tiles 
            # ie use the cascade classifiers to see on the board onto a seperate array and compare that to what the dumb thing sees 
            # use the mapping of the last board to place the newest piece onto the self.last_board_array/remove killed pieces (with corners) and with correct color
            # previous step needs last_board_array to correctly determine what to do with points
            # if all else fails use the boolean "is_black_turn" to color the tiles. 
            # Should be around a 100% accuracy with smart players and a highish accuracy with dumb players and good lighting conditions. 
            self.last_board_array = ...
            
        else:
            self.last_board_array = cascade_output
        
        self.last_board_image = image
        return self.last_board_array

image = standardizeImage("./resources/a.png")
roy_model = GoModel(19)
# print(roy_model.readBoard(image))
roy_model.showBoard(image)
# Figure out rotation code