import yadisk
import shutil

WHOLE_CLUBS = []

Y = yadisk.YaDisk(token='y0_AgAAAABgt50kAAueLgAAAAEB5UX6AADCTODpCFZF4Y0MpRy-WEYGXMin8Q')

for el in Y.listdir('/'):
    WHOLE_CLUBS.append(el['name'])


def download_file_to_club(club, folder, file_name):
    if club in WHOLE_CLUBS:
        try:
            check_folder(club, folder)
            Y.upload(f'data/users_files/{folder}/{file_name}', f'{club}/{folder}/{file_name}')
        except Exception:
            print('Ошибка')

    shutil.rmtree(f'data/users_files/{folder}')


def check_folder(club, folder):
    the_inside = []

    for elem in Y.listdir(f'/{club}'):
        the_inside.append(elem['name'])

    if the_inside:
        if folder not in the_inside:
            Y.mkdir(f'/{club}/{folder}')
    else:
        Y.mkdir(f'/{club}/{folder}')