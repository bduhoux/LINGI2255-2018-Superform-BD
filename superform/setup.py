from setuptools import setup

setup(
    name='superform',
    packages=['superform'],
    include_package_data=True,
    install_requires=[
        'flask',
<<<<<<< HEAD
        'python3-saml',
        'sqlalchemy',
        'flask_sqlalchemy',
        'feedgen',
        'python-twitter'
    ]


=======
        'python3-saml', 'sqlalchemy',
        'flask-sqlalchemy',
        'python-twitter',
        'feedgen'
    ],
>>>>>>> 6d07995... Implement the RSS channel
)
