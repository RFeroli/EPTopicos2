from ast import literal_eval


import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def plota_grafico(label, lao, iteracao):
    problema_numero = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    plt.plot(problema_numero, lao, color='green', label='LAO*')
    plt.plot(problema_numero, iteracao, color='orange', label='Iteraçao de valor')
    plt.xlabel('Problema navigation')
    plt.ylabel('Tempo em segundos')
    plt.yscale('log')
    plt.title(label)
    plt.legend()
    plt.show()



problema_d_r = {'deterministico':('Comparação dos dois algoritmos em segundos para cada problema determinístico',
                                  [0.3282332420349121,
                                   5.435866594314575,
                                   24.228187084197998,
                                   98.48492789268494,
                                   232.16284799575806,
                                   525.806342124939,
                                   828.287113904953,
                                   1248.0351510047913,
                                   2179.1152563095093,
                                   3462.7137422561646],
                                    [0.18513083457946777,
                                    1.445026159286499,
                                    5.267740488052368,
                                    13.140328645706177,
                                    26.315667629241943,
                                    46.2308132648468,
                                    74.15466976165771,
                                    113.35748767852783,
                                    153.94130420684814,
                                    222.19576835632324]
                                  ),
                'random': ('Comparação dos dois algoritmos em segundos para cada problema aleatório',
                           [0.3372523784637451,
                            4.786386966705322,
                            27.74968981742859,
                            114.16908097267151,
                            233.10751461982727,
                            579.8687291145325,
                            1341.8327701091766,
                            1992.1384749412537,
                            3633.357805967331,
                            3828.6400463581085],
                           [0.15010643005371094,
                            1.0547571182250977,
                            3.379412889480591,
                            9.366518497467041,
                            18.600189685821533,
                            36.117661476135254,
                            49.29899835586548,
                            80.26599192619324,
                            148.4504051208496,
                            177.08492732048035]
                                   )
                }






for p in problema_d_r:
    plota_grafico(problema_d_r[p][0], problema_d_r[p][1], problema_d_r[p][2])
