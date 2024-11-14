from tempfile import NamedTemporaryFile

from yaml import dump

from pytest import fixture

from pt_exporter.crawlers import Crawlers

@fixture(name='configuation_file_path', scope='session')
def _configuration_file_path():
    with NamedTemporaryFile('w', delete=False) as file:
        dump(
            {
                'crawlers': [
                    {
                        'headers': {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                        },
                        'class': 'MTeam',
                        'base_url': '',
                    }
                ]
            },
            file
        )
        return file.name

@fixture(name='crawlers', scope='session')
def _crawlers(configuation_file_path):
    return Crawlers(configuation_file_path)

def test_get_users(crawlers):
    for website, user in crawlers.get_users().items():
        print(website, user)
