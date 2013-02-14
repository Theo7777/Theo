from setuptools import setup, find_packages

version = '2.2.2'

setup(name='django-staticfiles-bootstrap',
      version=version,
      description="Twitter Bootstrap staticfiles for django",
      long_description=open("README.md", "r").read(),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Framework :: Django",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP",
          ],
      keywords='',
      author='Scott Rubin',
      author_email='apreche@frontrowcrew.com',
      url='http://github.com/apreche/django-staticfiles-bootstrap',
      license='MIT',
      packages=find_packages(),
      install_requires = [],
      include_package_data=True,
      zip_safe=False,
    )
