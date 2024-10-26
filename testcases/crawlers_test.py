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
                        'header-file-path': './headers/mteam.header',
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
