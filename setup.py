from setuptools import setup, find_packages

setup(
    name="geomapper",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "folium",
        "uvicorn",
    ],
)
