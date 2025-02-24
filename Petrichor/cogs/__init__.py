from pkgutil import iter_modules

EXCLUDED_EXTENSIONS = [
    'reminders',
    'sample'
]

EXTENSIONS = [
    module.name 
    for module 
    in iter_modules(__path__, f'{__package__}.')
    if module.name.split('.')[-1] not in EXCLUDED_EXTENSIONS
]