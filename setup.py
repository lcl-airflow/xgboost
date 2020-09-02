from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['xgboost==1.2.0',
                    'numpy==1.18.5',
                    'scipy==1.4.1',
                    'pandas==0.25.3']

setup(
    name='xgboost_mlops',
    version='1.0.0',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='xgboost distributed training example'
)