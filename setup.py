import setuptools



setuptools.setup(
    name="PPY_Poject_2023",
    version="1.0.0",
    author="Oleksandr Sokil, Anton Makhniuk",
    author_email="s25416@pjwstk.edu.pl,s24379@pjwstk.edu.pl",
    description="Web Media Catalog Service",
    url="https://github.com/AntonMakhniuk/PPY_Project_2023",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "nonion==0.4.4",
    ],
)