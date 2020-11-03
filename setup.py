from distutils.core import setup

setup(
    name='easyai',
    packages=['easyai'],
    version='0.1',
    license='MIT License',
    description='This package contains classes of pre-written Tensorflow models and functions '
                'to interact with them for students to play with and learn about the core high level concepts of AI.',
    author='Vincent Quirion',
    author_email='vincent.quirion@icloud.com',
    url='https://github.com/user/reponame',  # Provide either the link to your github or to your website
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',  # I explain this later on
    keywords=['ai', 'student', 'beginner', 'tensorflow', 'highschool', 'mnist'],
    install_requires=[
        'tensorflow',
        'numpy',
        'matplotlib',
        'opencv-python',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Students',
        'Topic :: Software Development :: Build Tools',
        'License :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
