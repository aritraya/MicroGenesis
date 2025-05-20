from setuptools import setup, find_packages

# Read requirements
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip()]

# Read dev requirements
with open("requirements-dev.txt") as f:
    dev_requirements = [line.strip() for line in f if line.strip()]

setup(
    name="microgenesis",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    description="MicroGenesis Python Project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="YourName",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/microgenesis",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
    },
    entry_points={
        "console_scripts": [
            "microgenesis=microgenesis.main:main",
        ],
    },
    include_package_data=True,
)
