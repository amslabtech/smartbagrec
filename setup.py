from setuptools import setup, find_packages

print(find_packages())
setup(
    name="smartbagrec",
    version="1.0",
    license="MIT",
    description="GUI based application to record rosbag files.",
    author="Yasunori Hirakawa",
    url="https://github.com/amslabtech/smartbagrec.git",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "bagrec = smartbagrec_cli.bagrec:main"
        ]
    }
)
