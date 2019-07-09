'''
    Configuration file parser.
'''
import os
WC3_KEY = 'Warcraft III.exe path'
SRC_KEY = 'Map folder path'
DST_KEY = 'Build folder path'

CONF_TEMPLATE = WC3_KEY + ': \"\"\n' + SRC_KEY + ': \"\"\n' + DST_KEY + ': \"\"'

def get_paths(conf_path):
    '''
        Function returns paths to Warcraft III.exe, source folder and destination folder.
    '''
    if not os.path.exists(conf_path):
        print('Can not find \'config.txt\'. Generating new one.')
        with open(conf_path, 'w') as conf_file:
            conf_file.write(CONF_TEMPLATE)

    with open(conf_path, 'r') as conf_file:
        for line in conf_file.readlines():
            if line.find(WC3_KEY) > -1:
                war3_path = line[line.find('\"') + 1:line.rfind('\"')]
                continue
            if line.find(SRC_KEY) > -1:
                src_path = line[line.find('\"') + 1:line.rfind('\"')]
                continue
            if line.find(DST_KEY) > -1:
                dst_path = line[line.find('\"') + 1:line.rfind('\"')]
                continue

    done = True
    if src_path is None or not os.path.exists(src_path):
        print('Can not find source folder (' + src_path + '). Check configuration file.')
        done = False
    if dst_path is None or not os.path.exists(dst_path):
        print('Can not find destination folder (' + dst_path + '). Check configuration file.')
        done = False
    if not done:
        return None, None, None

    return war3_path, src_path, dst_path
