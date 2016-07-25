import os
import copy
from zc.buildout.buildout import _open, _update, _unannotate


def ext(buildout):
    # get substituted value of extends-subs in buildout section
    extends_subs = buildout['buildout'].get('extends-subs')
    if extends_subs:
        # get data from the buildout
        data = buildout._annotated.copy()
        raw_data = buildout._raw.copy()
        buildout_dir = buildout['buildout']['directory']
        # get stored command-line options
        cloptions = dict([
            ('buildout',
             dict([
                (k, v) for k, v in data['buildout'].items() 
                if v[1] == 'COMMAND_LINE_VALUE'
             ])
            ),
        ])
        override = cloptions.get('buildout', {}).copy()
        # get dl_options from buildout
        dl_options = data['buildout'].copy()
        
        # open multiple cfg files in extends-subs to produce result dict
        extends_subs = extends_subs.split()
        filename = extends_subs.pop(0)
        result = _open(buildout_dir, filename, [], dl_options, override,
                        set())
        for fname in extends_subs:
            _update(result, _open(buildout_dir, fname, [], dl_options, override,
                    set()))
        
        # update data from new result
        _update(data, result)
        # apply command-line options
        _update(data, cloptions)
        
        # reset buildout data and update each section
        buildout._data = {}
        buildout._annotated = copy.deepcopy(data)
        buildout._raw.update(_unannotate(data))
        # WORKAROUND: fix absolute path for develop-eggs-directory
        buildout._raw['buildout']['develop-eggs-directory'] = raw_data['buildout']['develop-eggs-directory']
        for section in buildout._raw.keys():
            buildout[section]            
        