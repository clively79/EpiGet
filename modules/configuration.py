import json
import sys


class Configuration:
    def __init__(self, settings):
        self.ver = settings['ver']
        self.port = settings['port']
        self.api_key = settings['API-Key']
        self.library_path = settings['library-path']
        self.torrent_path = settings['library-path']
        self.download_path = settings['download-path']

    @staticmethod
    def configure():
        import os
        if 'help' in sys.argv:
            file = open('confighelp', 'r')
            print(file.read())
            file.close()

        def getport(str):
            p = input(f'{str} (1025-65535) default 5555: ')
            if p == '' or not p.isnumeric() or int(p) < 1025 or int(p) > 65535 or not isinstance(p, int):
                return 5555

        def getpath(str):
            temp = input(f'{str} :')
            path = temp if temp[-1] == '/' else temp + '/'

            try:
                open(path + 'test.conf', 'w')
            except:
                raise('Unable to write to path provided. Verify that EpiGet has permission to write to the specified directory and rerun configuration')
            else:
                os.remove(path +'test.conf')

            return path

        configuration = {
            'ver': 0.01,
            'port': 0,
            'API-Key': '',
            'library-path': '',
            'torrent-path': '',
            'download-path': ''
        }

        functions = {
            'ver': lambda a: configuration[a],
            'port': lambda a: configuration[a] + getport(a),
            'API-Key': lambda a: configuration[a] + input(f'{a}: '),
            'library-path': lambda a: configuration[a] + getpath(a),
            'torrent-path': lambda a: configuration[a] + getpath(a),
            'download-path': lambda a: configuration[a] + getpath(a)
        }

        for key in configuration:
            configuration[key] = functions[key](key)

        configfile = open('config.json', 'w')
        configfile.write(json.dumps(configuration, indent=4))
        configfile.close()


if __name__ == '__main__':
    raise Exception('config object cannot be run as __main__')
