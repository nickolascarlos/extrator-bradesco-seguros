import cv2
import numpy as np
from matplotlib import pyplot as plt

from aux import is_row_of_interest

image = cv2.imread("/home/nickolas/Imagens/cilia.jpg", 0)

def shw(img):
    plt.title('Imagem')
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()

table = image[750:, :]

_,table_thresh = cv2.threshold(table, 240, 255, cv2.THRESH_BINARY_INV)

median_blur_table = cv2.medianBlur(table_thresh, 11, 0)

kernel_e = cv2.getStructuringElement(cv2.MORPH_RECT, (table.shape[1]//60, table.shape[0]//60))
eroded_table = cv2.erode(median_blur_table, kernel_e)
dilated_table = cv2.dilate(eroded_table, kernel_e)

# Blobs edges
table_edges = cv2.Canny(dilated_table, 30, 150)

# Bordas horizontais:
kernel_horizontal_lines = cv2.getStructuringElement(cv2.MORPH_RECT, (table.shape[1]//60, 1))
hor_edges = cv2.erode(table_edges, kernel_horizontal_lines)
hor_edges = cv2.dilate(hor_edges, kernel_horizontal_lines)

# Bordas verticais:
kernel_vertical_lines = cv2.getStructuringElement(cv2.MORPH_RECT, (1, table.shape[0]//60))
vert_edges = cv2.erode(table_edges, kernel_vertical_lines)
vert_edges = cv2.dilate(vert_edges, cv2.getStructuringElement(cv2.MORPH_RECT, (1, table.shape[0]//15)))

# Estrutura da tabela: combinação bordas verticais + horizontais
cbon = cv2.bitwise_or(hor_edges, vert_edges)
cbon = cv2.dilate(cbon, cv2.getStructuringElement(cv2.MORPH_RECT, (table.shape[1]//80, table.shape[0]//80)))
cbon = cv2.erode(cbon, cv2.getStructuringElement(cv2.MORPH_RECT, (table.shape[1]//90, table.shape[0]//90)))

contours, _ = cv2.findContours(cbon, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

drawable_image = cv2.imread("/home/nickolas/Imagens/cilia.jpg", 1)

 # Linhas:
table_rows = []
table_rows_contours = []
for curr_contour in contours:
    x,y,w,h = cv2.boundingRect(curr_contour)
    if w*h <= 300000:
        table_row = table[y:y+h, x:x+w]
        table_rows.append(table_row)
        table_rows_contours.append(curr_contour)

# Transforma as linhas (já binarizadas) em uma imagem que se assemelha a um código de barras
# para determinar se ela é ou não uma linha de interesse
treated_rows = []
for (i, table_row) in enumerate(table_rows):
        _, thresh_table = cv2.threshold(table_row, 190, 255, cv2.THRESH_BINARY_INV)
        dilated_table_row = cv2.dilate(thresh_table, cv2.getStructuringElement(cv2.MORPH_RECT, (h//4, w//4)))
        m_tab_r = cv2.blur(dilated_table_row, (5,5), 0)
        _, m_tab_r = cv2.threshold(m_tab_r, 20, 255, cv2.THRESH_BINARY)

        treated_rows.append(m_tab_r)

# Varre todas as linhas da tabela e mostra se é ou não uma linha de interesse
# for (i,row) in enumerate(treated_rows):
#     row_t = cv2.resize(row, (500, 10), interpolation = cv2.INTER_NEAREST)
#     print("Linha nº %d %s" % (i, "é uma linha de interesse" if is_row_of_interest(row_t) else "NÃO é uma linha de interesse"))

# Desenha
drawable_image = cv2.imread("/home/nickolas/Imagens/cilia.jpg", 1)
for (i, row) in enumerate(treated_rows):
    row_t = cv2.resize(row, (500, 10), interpolation = cv2.INTER_NEAREST)
    _contour_ = table_rows_contours[i]
    x,y,w,h = cv2.boundingRect(_contour_)
    drawable_image = cv2.rectangle(drawable_image, (x,y+750), (x+w,y+750+h), (0,255,0) if is_row_of_interest(row_t) else (0,0,255), 7)

shw(drawable_image)



