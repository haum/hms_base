from distutils.core import setup

setup(
    name='hms_base',
    version='1.0',
    packages=['hms_base', 'hms_base.tests'],
    url='https://github.com/haum/hms_base',
    license='MIT',
    author='Romain Porte (microjoe)',
    author_email='microjoe@microjoe.org',
    description='Base package for HAUM micro-services',
    install_requires=['pika']
)
