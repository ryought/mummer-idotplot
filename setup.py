from setuptools import setup

setup(
        name="mummer-idotplot",
        version="0.0.1",
        install_requires=["plotly"],
        entry_points={
            "console_scripts": [
                "mummer-idotplot = mummer_idotplot.main:main"
                ]
            }
        )
