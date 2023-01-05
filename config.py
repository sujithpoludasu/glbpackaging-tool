VALID_PROJECTS= ['cool']
SERVER_PATH = 'j:/'
PROJECTS = {
    'cool': {
        'roto':
            {
                'file_format': '.exr',
                'len_split': 4,
                'task_split': '_roto_',
                'input_split': 4,
                'valid_tasks': ['arms', 'char', 'dress', 'face']
                },
        'paint':
            {
                'file_format': '.exr',
                'len_split': 3,
                },

            },

    'Manifest': {
            'roto':
                {
                    'file_format': '.exr',
                    'len_split': 3,
                    'task_split': '_roto', # 'PMS2_203_203-016-116_rotoMP-WR-01_v001.%04d.exr' it is used to split the shotname and task
                    'input_split': 3, # 'PMS2_203_203-016-116_MP-WR_v001.1001 this is to get the shot name from inputpath
                    'valid_tasks': ['arms', 'char', 'dress', 'face']
                    },
            'paint':
                {
                    'file_format': '.exr',
                    'len_split': 3,
                    'input_split': 3, # 'PMS2_203_203-016-116_MP-WR_v001.1001 this is to get the shot name from inputpath
                    },

                },

}

