from setuptools import setup, find_packages

setup(
    name="dapiclient",
    version="1.3.0",
    description="A Python client SDK for DASH Platform",
    long_description=open('README.md').read(),  # Assuming you have a README.md
    long_description_content_type="text/markdown",
    author="mayoreee",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "base58>=2.1.0",
        "cbor2>=5.4.0",
        "certifi>=2021.5.30",
        "charset-normalizer>=2.0.3",
        "grpcio>=1.38.1",
        "idna>=3.2",
        "protobuf>=3.17.3",
        "requests>=2.26.0",
        "six>=1.16.0",
        "urllib3>=1.26.6",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.9',
    url="https://github.com/mayoreee/dapi-client-py",
    project_urls={
        "Homepage": "https://github.com/mayoreee/dapi-client-py",
        "Repository": "https://github.com/mayoreee/dapi-client-py",
    },
)
