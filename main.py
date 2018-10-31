import argparse
from owslib.wfs import WebFeatureService

# wfs = WebFeatureService(
#    url='http://geodata.nationaalgeoregister.nl/brocpt/wfs',
#    version='1.1.0'
# )

default_format = 'json'
default_limit = None
default_url = 'https://geodata.nationaalgeoregister.nl/bodemkaart50000/wfs'

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--format', default=default_format)
parser.add_argument('-l', '--limit', default=default_limit)
parser.add_argument('-u', '--url', default=default_url)

args = parser.parse_args()

format = args.format
limit = args.limit
url = args.url

print('args', args)

wfs = WebFeatureService(
    url=url,
    version='1.1.0'
)

contents = list(wfs.contents)


def log(message):
    print('--')
    print(message)
    print('----------\n')


def get_feature(content):
    try:
        return wfs.getfeature(
            maxfeatures=None,
            srsname='EPSG:4326',
            typename=content,
            outputFormat=format
        )
    except Exception as e:
        exit(e)


for idx, content in enumerate(contents):
    log('Getting features of ' + content)
    file = open('output/output_' + content + '.' + format, 'w')
    response = get_feature(content)
    log('Writing features of ' + content + ' to file')

    value = None

    try:
        value = response.getvalue()
    except Exception as e:
        print(e)

    if (value is not None):
        file.write(response.getvalue())

exit()
