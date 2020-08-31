from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['scikit-learn==0.22','xgboost','numpy','scipy','Flask','pandas==0.25.3', 'tensorflow==1.14.*']

setup(
    name='xgboost',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='xgboost distributed training example'
)