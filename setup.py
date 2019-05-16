from setuptools import setup, find_packages

setup(
    name='lightdataparser',
    version=0.7,
    license='MIT',
    author='xenking',
    author_email='xenkings@gmail.com',
    url='https://github.com/XENKing/lightdataparser',
    description="Simple application (Extract, Transform, Load) for data organizing",
    long_description="README.md",
    test_suite='lightdataparser.tests.test_all',
    install_requires=['pyforms-gui'],
    packages=find_packages(),
    package_dir={'lightdataparser': 'lightdataparser'},
    package_data={'lightdataparser.gui': ['styles.css']},
    include_package_data=True,
    entry_points={'console_scripts': ['lightdataparser = lightdataparser.main:main',
                                      'lightdataparser-gui = lightdataparser.gui.app:start_gui']}
)
