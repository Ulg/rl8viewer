import ctypes
from io import SEEK_CUR

import matplotlib.pyplot as plt

from rlview import rli_file



def main():

    file = rli_file.RLIFile('data/РЛС-А100-аэропорт.rl4')
    file.add('data/РЛС-А200-аэропорт.rl4')
    
    img = file.toimg()
    plt.imshow(img, cmap='gray')
    plt.show()



    # headers = {}
    # headers['data/РЛС-А100-аэропорт.rl4'] = rli_file.get_header('data/РЛС-А100-аэропорт.rl4')
    # headers['data/РЛС-А200-аэропорт.rl4'] = rli_file.get_header('data/РЛС-А200-аэропорт.rl4')
    # headers['data/РЛС-А300-аэропорт.rl4'] = rli_file.get_header('data/РЛС-А300-аэропорт.rl4')
    # headers['data/РЛС-А400-аэропорт.rl4'] = rli_file.get_header('data/РЛС-А400-аэропорт.rl4')

    # for key in headers:
    #     print(f'sx: {headers[key].RLIFileParams.sx}, sy: {headers[key].RLIFileParams.sy}')
    #     print(f'Lambda: {headers[key].SynthParams.Lambda}')

    # rli_file.RLIFile('data/РЛС-А100-аэропорт.rl4').toimg()
    # rli_file.RLIFile('data/РЛС-А200-аэропорт.rl4').toimg()
    # rli_file.RLIFile('data/РЛС-А300-аэропорт.rl4').toimg()
    # rli_file.RLIFile('data/РЛС-А400-аэропорт.rl4').toimg()

    # rli_file.RLIFile.test('data/РЛС-А100-аэропорт.rl4')
    # print()
    # rli_file.RLIFile.test('data/РЛС-А200-аэропорт.rl4')
    # print()
    # rli_file.RLIFile.test('data/РЛС-А300-аэропорт.rl4')
    # print()
    # rli_file.RLIFile.test('data/РЛС-А400-аэропорт.rl4')


if __name__ == '__main__':
    main()
