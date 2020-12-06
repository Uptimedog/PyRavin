import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyravin",
    version="0.0.5",
    author="clivern",
    author_email="hello@clivern.com",
    description="Apache License, Version 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GeometryIO/PyRavin",
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        "requests>=2.25.0",
        "pytz>=2020.4",
        "google-api-python-client>=1.12.8",
        "google-auth>=1.23.0",
        "google-auth-oauthlib>=0.4.2",
        "google-auth-httplib2>=0.0.4"
    ],
    license="Apache License, Version 2.0",
    platforms=['any'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
)
