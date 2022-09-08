from setuptools import setup

setup(name='gym-sf',
      version='0.0.1',
      description='Environments adapted to the use of successor features',
      author="Rafael F Cunha",
      author_email="rafaelcunha2013@gmail.com",
      python_requires=">=3.8",
      install_requires=['gym==0.25.2',
                        'numpy',
                        'pygame==2.1.2']
      )
