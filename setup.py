import setuptools




setuptools.setup(
    name="PPY_Poject_2023",
    version="1.0.0",
    author="Oleksandr Sokil, Anton Makhniuk",
    author_email="s25416@pjwstk.edu.pl,",
    description="Web Media Catalog Service,s24379@pjwsi.edu.pl",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "nonion==0.4.4",
    ],
)