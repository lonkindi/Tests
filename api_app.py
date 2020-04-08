import requests
import requests.exceptions

API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


def translate_it(s_text, a_key=API_KEY, a_url=URL):
    params = {
        'key': a_key,
        'text': s_text,
        'lang': '{}-{}'.format('en', 'ru'),
    }
    # try:
    response = requests.get(a_url, params=params)
    return response
    # except requests.exceptions.MissingSchema as err:
    #     return err



if __name__ == '__main__':
    print(translate_it('A', 'B', 'C', 'D'))
