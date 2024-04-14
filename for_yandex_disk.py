import yadisk


def download_file_to_club(club, folder, file_name, file):
    whole_clubs = []

    y = yadisk.YaDisk(token='y0_AgAAAABgt50kAAueLgAAAAEB5UX6AADCTODpCFZF4Y0MpRy-WEYGXMin8Q')

    for el in y.listdir('/'):
        whole_clubs.append(el['name'])

    if club in whole_clubs:
        print(True)
    else:
        print(False)

    print(f'{club}/{folder}/{file_name}')


# download_file_to_club('Зимняя Сказка 2')
