from setuptools import setup

setup(
    name='lightdataparser',
    version=0.5,
    license='MIT',
    author='xenking',
    author_email='xenkings@gmail.com',
    url='https://github.com/XENKing/lightdataparser',
    description="Simple application (Extract, Transform, Load) for data organizing",
    long_description="README.md",
    packages=['lightdataparser'],
    include_package_data=True,
    entry_points={'console_scripts': ['lightdataparser = lightdataparser.main:main']}
)
