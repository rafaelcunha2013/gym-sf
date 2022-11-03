from setuptools import setup, find_packages

packages = [package for package in find_packages() if package.startswith("gym_sf")]

setup(name='gym-sf',
      version='0.0.5',
      description='Environments adapted to the use of successor features',
      author="Rafael F Cunha",
      author_email="rafaelcunha2013@gmail.com",
      url="https://github.com/rafaelcunha2013/gym-sf",
      license='MIT',
      packages=packages,
      python_requires=">=3.8",
      install_requires=['gym==0.25.2',
                        'numpy',
                        'pygame==2.1.2']
      )

# https://www.gymlibrary.dev/content/environment_creation/
# https://towardsdatascience.com/create-your-own-python-package-and-publish-it-into-pypi-9306a29bc116

