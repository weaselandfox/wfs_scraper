import argparse
from owslib.wfs import WebFeatureService

# wfs = WebFeatureService(
#    url='http://geodata.nationaalgeoregister.nl/brocpt/wfs',
#    version='1.1.0'
# )

default_format = None
default_limit = None
default_url = 'https://geodata.nationaalgeoregister.nl/bodemkaart50000/wfs'
default_content = None

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--format', default=default_format)
parser.add_argument('-l', '--limit', default=default_limit)
parser.add_argument('-u', '--url', default=default_url)
parser.add_argument('-c', '--content', default=default_content)

args = parser.parse_args()

format = args.format
limit = args.limit
url = args.url
content = args.content

print('args', args)

wfs = WebFeatureService(
    url=url,
    version='1.1.0'
)

contents = list(wfs.contents)

if (content is not None):
    contents = [content]


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

    extension = '.' + format if format is not None else ''
    file = open('output/output_' + content + extension, 'w')
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
