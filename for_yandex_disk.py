import yadisk
import shutil

WHOLE_CLUBS = []

Y = yadisk.YaDisk(token='y0_AgAAAABgt50kAAueLgAAAAEB5UX6AADCTODpCFZF4Y0MpRy-WEYGXMin8Q')

for el in Y.listdir('/'):
    WHOLE_CLUBS.append(el['name'])


def download_file_to_club(club, folder, file_name):
    if club in WHOLE_CLUBS:
        Y.upload(f'data/users_files/{folder}/{file_name}', f'{club}/{folder}/{file_name}')
        shutil.rmtree(f'data/users_files/{folder}')


def check_file_in_folder(club, folder, file_name):
    for el in Y.listdir(f'/{club}'):
        print(el['name'])


download_file_to_club('Маленькая принцесса 2024', 'Кочак Эфе', 'Minecraft2.mp3')