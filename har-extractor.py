import json
import sys
from typing import List
import base64


def main():
    if len(sys.argv) != 2:
        print('No HAR file is specified.')
        return

    file_name: str = sys.argv[1]
    json_content: dict
    try:
        with open(file_name, 'r') as json_file:
            json_content = json.load(json_file)
    except Exception as ex:
        print(ex)
        return
    logs: dict = json_content['log']
    entries: List[dict] = logs['entries']

    index: int = 0

    for entry in entries:
        response = entry['response']
        status: int = response['status']
        if status != 200:
            continue
        content: dict = response['content']
        mime_type: str = content['mimeType']
        content_text: str = content.get('text')
        encode: str = content.get('encoding')
        if mime_type == 'image/jpeg' and encode == 'base64':
            data = base64.b64decode(content_text)
            with open('%03d.jpg' % index, 'wb') as out_file:
                out_file.write(data)
                out_file.close()
            index += 1
    print('%d image(s) was saved.' % (index + 1))


if __name__ == "__main__":
    main()
