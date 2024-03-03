from setuptools import find_packages, setup

REQUIRES = [
    'Django==5.0.2',
    'psycopg2-binary==2.9.9',
    'setuptools==69.1.1',
    'pip==24.0',
    'stripe==8.4.0',
    'python-dotenv==1.0.1',
]


CODESTYLE_REQUIRES = [
    'flake8==7.0.0',
    'isort==5.13.2',
]


setup(
    name='stripe_payments',
    packages=find_packages(),
    install_requires=REQUIRES,
    extras_require={'codestyle': CODESTYLE_REQUIRES}
)
