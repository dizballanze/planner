from setuptools import setup

setup(name='planner',
      version='0.1',
      description='Draw 2d plans of buildings',
      url='http://github.com/dizballanze/planner',
      author='Yuri Shikanov',
      author_email='dizballanze@gmail.com',
      license='MIT',
      packages=['planner', 'planner.frame'],
      install_requires=['svgwrite==1.1.6', 'shortuuid==0.4.2'],
      zip_safe=False)