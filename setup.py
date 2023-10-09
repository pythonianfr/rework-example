from pathlib import Path
from setuptools import setup


doc = Path(__file__).parent / 'README.md'


setup(name='rework-example',
      version='0.1.0',
      author='Aurelien Campeas',
      author_email='aurelien.campeas@pythonian.fr',
      description='A repo providing basic code examples of rework use ',
      long_description=doc.read_text(),
      long_description_content_type='text/markdown',
      url='https://github.com/pythonianfr/rework-example',
      packages=['example'],
      zip_safe=False,
      install_requires=[
          'rework',
      ],
      entry_points={
          'console_scripts': [
              'example=example.cli:example'
          ]
      }
)
