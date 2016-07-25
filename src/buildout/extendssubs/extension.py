import os
import copy

from zc.buildout import configparser
from zc.buildout.buildout import _save_options, _default_globals

subs_cfg_filename = '.subs.cfg'

def ext(buildout):
    # get substituted value of extends-subs in buildout section
    extends_subs = buildout['buildout'].get('extends-subs')
    if extends_subs:
        # get running config_file stored as note of extends-subs option
        # inside buildout's _annotated dict
        filename = buildout._annotated['buildout']['extends-subs'][1]
        fp = open(filename)
        # get parsed result of running config_file
        result = configparser.parse(fp, '', _default_globals)
        fp.close()
        
        # add value of extends-subs into extends option
        result['buildout']['extends'] = ' '.join(
            (result['buildout'].get('extends', ''),
             buildout['buildout']['extends-subs']
            )).strip()
        
        # write updated result of config_file into new .subs.cfg file
        f = open(subs_cfg_filename, 'w')
        # make sure buildout section always go first
        _save_options('buildout', result['buildout'], f)
        for section in result.keys():
            if section != 'buildout':
                _save_options(section, result[section], f)
        f.close()

        # get command-line options stored in buildout._annotated
        options = [
            ('buildout', k, v[0]) 
            for k, v in buildout._annotated['buildout'].items() 
            if v[1] == 'COMMAND_LINE_VALUE'
        ]
        
        # re-initialize buildout obj with new cfg file
        buildout.__init__(subs_cfg_filename, options,
                          user_defaults=True,
                          command='install', args=())

        # FIX: remove duplicated log handler
        if len(buildout._logger.handlers) == 2:
            buildout._logger.removeHandler(buildout._logger.handlers[1])
