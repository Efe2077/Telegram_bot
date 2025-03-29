import yadisk


WHOLE_CLUBS = []

Y = yadisk.YaDisk(token='y0__xC15kcY9IM1IJaZ39USvGCqQxg1HS9DHvtCd7qU-umxzzQ')


for el in Y.listdir('/Music'):
    WHOLE_CLUBS.append(el['name'])


def download_file_to_club(club, file_name):
    try:
        if club in WHOLE_CLUBS:
            try:
                # Загружаем файл на Яндекс.Диск
                Y.upload(file_name, f'/Music/{club}/{file_name}')
                return True
            except Exception:
                return False
    except Exception:
        print('download_file_to_club сбоит')


# def check_folder(club):
#     try:
#         the_inside = []
#
#         for elem in Y.listdir(f'/{club}'):
#             the_inside.append(elem['name'])
#
#         if the_inside:
#             if folder not in the_inside:
#                 Y.mkdir(f'/{club}/{folder}')
#         else:
#             Y.mkdir(f'/{club}/{folder}')
#     except Exception:
#         print('check_folder сбоит')
# # Тут добавление файлов в Яндекс.Диск