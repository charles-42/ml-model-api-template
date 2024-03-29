from setuptools import setup, find_packages


setup(
    name="ML_master",
    version="0.5",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "pickle-mixin",   
    ],
    # Metadata
    author="Petrov Evgeni",
    author_email="Jetestcreationpackage@hotmail.com",
    description="Ceci est un test de création d'un package python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/charles-42/ml-model-api-template.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

