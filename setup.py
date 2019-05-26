from setuptools import setup

setup(
        name="mummer-idotplot",
        version="0.1.2",
        description="Generate interactive dotplot from mummer4 output using plotly",
        long_description=open('README.md').read(),
        long_description_content_type="text/markdown",
        url="https://github.com/ryought/mummer-idotplot",
        author="ryought",
        author_email="ryonakabayashi@gmail.com",
        license="MIT",
        packages=[
            "mummer_idotplot",
            ],
        install_requires=["plotly"],
        entry_points={
            "console_scripts": [
                "mummer-idotplot = mummer_idotplot.main:main"
                ]
            }
        )
