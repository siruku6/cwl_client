from setuptools import setup, find_packages
# import sys

# sys.path.append('./cwl_client')
# sys.path.append('./tests')

setup(
    name='cwl_client',
    url='https://github.com/siruku6/cwl_client',
    version='0.0.1',
    description='This is the client for AWS CloudWatch Logs',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    # test_suite = 'test_interface.suite',
    author='siruku6',
    python_requires='>=3.7',
    install_requires=get_requirements('requirements.txt'),
    license='MIT',
)
