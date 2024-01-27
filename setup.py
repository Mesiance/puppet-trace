from setuptools import setup, find_packages

setup(
    name="puppet-trace",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["PyYAML==6.0", "python-dotenv==1.0.0"],
    entry_points={
        "console_scripts": [
            "puppet-trace=puppet_trace.main:main",
        ],
    },
)
