from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
    long_description = long_description.replace("\r", "")
except:
    long_description = ''

setup(
    name='sanic_brogz',
    version='0.1.1',
    description='An extension which allows you to easily brotli comprss or gzip your Sanic responses.',
    long_description=long_description,
    url='http://github.com/bitpartio/sanic_brogz',
    author='Michael Chisari',
    license='MIT',
    packages=['sanic_brogz'],
    install_requires=('sanic', 'brotli'),
    zip_safe=False,
    keywords=['sanic', 'gzip', 'brotli'],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Session',
    ]
)
