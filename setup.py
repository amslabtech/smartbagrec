from setuptools import setup

setup(
    name="smartbagrec",
    version="1.0",
    license="MIT",
    description="GUI based application to record rosbag files.",
    author="Yasunori Hirakawa",
    url="https://github.com/YasunoriHirakawa/smartbagrec.git",
    packages=["smartbagrec"],
    entry_points={
        "console_scripts": [
            "bagrec = smartbagrec.bagrec:main"
        ]
    }
)
