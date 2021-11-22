'''
    Função para determinar se uma dada linha da tabela é ou não uma célula de interesse.

    Recebe uma imagem de 500 x 1 como parâmetro.

    Checa se todos os pontos de interesse correspondem às cores (preto ou branco) esperadas.
    Tais cores (esperadas) foram determinadas com o bitwise_and de todas as linhas consideradas de interesse,
    obtendo assim as "regiões brancas" em comum em todas elas. Dessa forma, espera-se que toda célula de interesse
    tenha a mesma correspondência. Pode-se melhorar ainda mais essa função fazendo a mesma coisa paras as "regiões pretas",
    isso é, determinando as regiões pretas em comum em todas as linhas de interesse.
'''
def is_row_of_interest(image):
    x_list =     [5, 62, 72, 85, 93, 123, 135, 160, 300, 310, 350, 365, 400, 407, 440, 445, 490]
    x_expected = [255, 0,  255,  0,  255,  0,   255,   255,   0,   255,   0,   255,   0,   255,   0,   255,   0  ]

    for x in zip(x_list, x_expected):
        color_at_x = image[0][x[0]]
        if (color_at_x != x[1]):
            return False

    return True

''' Código utilizado para a determinação das "regiões brancas" em comum:
* Obs: Todas as linhas contidas em treated_rows eram consideradas linhas de interesse

# result = cv2.resize(treated_rows[0], (500, 10), interpolation = cv2.INTER_NEAREST)
# for row_index in range(1, len(treated_rows)):
#     row = cv2.resize(treated_rows[row_index], (500, 10), interpolation = cv2.INTER_NEAREST)
#     result = cv2.bitwise_and(result, row)

# shw(result)
'''
