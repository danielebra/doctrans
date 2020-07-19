docstring_structure = {
    'short_description': 'Acquire from the official tensorflow_datasets '
                         'model zoo, or the ophthalmology focussed '
                         'ml-prepare library',
    'long_description': '',
    'params': [
        {
            'default': 'mnist',
            'doc': 'name of dataset.',
            'name': 'dataset_name',
            'typ': 'str'
        },
        {
            'default': '~/tensorflow_datasets',
            'doc': 'directory to look for models in.',
            'name': 'tfds_dir',
            'typ': 'Optional[str]'
        },
        {
            'doc': 'backend engine, e.g., `np` or `tf`',
            'name': 'K',
            'typ': 'Union[np, tf]'
        },
        {
            'doc': 'Convert to numpy ndarrays',
            'name': 'as_numpy',
            'typ': 'Optional[bool]'
        },
        {
            'doc': 'pass this as arguments to data_loader '
                   'function',
            'name': 'data_loader_kwargs',
            'typ': '**data_loader_kwargs'
        }
    ],
    'returns': {
        'doc': 'Train and tests dataset splits',
        'name': 'return_type',
        'typ': 'Union[Tuple[tf.data.Dataset, tf.data.Dataset], '
               'Tuple[np.ndarray, np.ndarray]]'
    }
}

docstring_str = """
Acquire from the official tensorflow_datasets model zoo, or the ophthalmology focussed ml-prepare library

:param dataset_name: name of dataset. Defaults to mnist
:type dataset_name: ```str```

:param tfds_dir: directory to look for models in. Defaults to ~/tensorflow_datasets
:type tfds_dir: ```Optional[str]```

:param K: backend engine, e.g., `np` or `tf`. Defaults to np
:type K: ```Union[np, tf]```

:param as_numpy: Convert to numpy ndarrays
:type as_numpy: ```Optional[bool]```

:param data_loader_kwargs: pass this as arguments to data_loader function
:type data_loader_kwargs: ```**data_loader_kwargs```

:return: Train and tests dataset splits
:rtype: ```Union[Tuple[tf.data.Dataset, tf.data.Dataset], Tuple[np.ndarray, np.ndarray]]```
"""
