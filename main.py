# Main file of the architecture, calls upon all the other steps
# Author : Adrien Bolling

import os.path
import pretreatment as prt
import numpy as np
from PIL import Image
import cv2

source_photo_path = './'
source_photo_name = 'game'
source_photo_extension = '.png'
source_full = source_photo_path+source_photo_name+source_photo_extension


if not(os.path.isfile(source_photo_path+source_photo_name+source_photo_extension)):
    print('Veuillez déposer une photo de la partie sous le nom "'+source_photo_name+source_photo_extension+'" dans le répertoire '+source_photo_path)
    exit()

'''
Pre-Treatment and segmentation
'''


img, gray_blur = prt.read_img(source_full)

# Canny edge detection
edges = prt.auto_canny(gray_blur)

lines_list =[]
lines = cv2.HoughLinesP(
            edges, # Input edge image
            1, # Distance resolution in pixels
            np.pi/180, # Angle resolution in radians
            threshold=80, # Min number of votes for valid line
            minLineLength=4, # Min allowed length of line
            maxLineGap=15 # Max allowed gap between line for joining them
            )
# Iterate over points
for points in lines:
      # Extracted points nested in the list
    x1,y1,x2,y2=points[0]
    # Draw the lines joing the points
    # On the original image
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    # Maintain a simples lookup list for points
    lines_list.append([(x1,y1),(x2,y2)])

lines = np.reshape(lines, (-1, 2))
h, v = prt.hor_vert_lines(lines)
points = prt.intersections(h, v)

# Cluster intersection points
points = prt.cluster(points)
# Find corners
img_shape = np.shape(img)
points = prt.find_corners(points, (img_shape[1], img_shape[0]))
# Perspective transform
new_img = prt.four_point_transform(img, points)

board = prt.find_board()

if board is None:
    print("Aucun échiquier n'a éét trouvé sur la photo")
    exit()

squares = prt.split_board(board)
squares = np.array(squares)

# Save the cropped images in a subfolder for later use
for i in range(0,squares.shape[0]):
    data=squares[i]
    img_square = Image.fromarray(data, 'RGB')
    name = source_photo_name+'_square_'+str(i)
    img.save('./pre-treatment/cropped/'+name+'.jpg')


'''
Occupancy classification
'''

import occupancy_classification as occ_class

occupancies = []

for square_data in squares:
    square = Image.fromarray(square_data, 'RGB')

    #not implemented yet
    occupancy = occ_class.predict(square)

    occupancies.append(occupancy)

'''
Occupied squares classification
'''

import piece_classification as p_class

pieces = []

for occupancy,square_data in zip(occupancies,squares):
    square = Image.fromarray(square_data, 'RGB')

    #not implemenetd yet
    if occupancy == 'empty':
        piece = 'None'
    else:
        piece = p_class.predict(square)
    pieces.append(piece)


'''
Traduction in standard notation system
'''

pieces_dict = {'White Queen': 'Q',
               'White King': 'K',
               'White Bishop': 'B',
               'White Rook': 'R',
               'White Knight': 'N',
               'White Pawn': 'P',
               'Black Queen': 'q',
               'Black King': 'k',
               'Black Bishop': 'b',
               'Black Rook': 'r',
               'Black Knight': 'n',
               'Black Pawn': 'p',}

mapped_pieces = [pieces_dict.get(case) if pieces_dict.get(case) else case for case in pieces]

mapped_pieces = np.array(mapped_pieces)
mapped_pieces = np.reshape(mapped_pieces, (8,8))

lines = []

for i in range(8):
    line = ""
    k = 0
    for j in range(8):
        if pieces[i,j] == 'None':
            k = k+1
        else:
            if k != 0:
                line = line + str(k)
            k=0
            line = line + pieces[i,j]
    lines.append(line)

final_board = "/"
for l in lines:
    final_board = final_board+l+"/"

'''
Display the board
'''

import chess
import chess.svg

board = chess.Board(final_board)

boardsvg = chess.svg.board(board, size=400)


'''
Save the result
'''
name = "board_picture"
outputfile = open(name+".svg", "w")
outputfile.write(boardsvg)
outputfile.close()

boardsvg