from setuptools import setup

setup(
    name='I2c7SegmentLed',
    version='1.0.1',
    description='Raspberry Pi software library for controlling 7 Segment LEDs using AMS AS1115 chip',
    long_description=open('README.md').read(),
    url='https://github.com/dcityorg/i2c-7-segment-led-library-raspberrypi',
    author='Gary Muhonen',
    author_email='gary@dcity.org',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: System :: Hardware',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='RPi AMS AS1115 I2C interface LED Seven Segment',
    py_modules=['I2c7SegmentLed'],
    install_requires=['smbus'],    
)