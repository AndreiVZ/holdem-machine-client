import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="holdem-machine-client",
    version="0.0.1",
    author="Python Strategies",
    author_email="pythonstrats@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AndreiVZ/holdem-machine-client",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy>=1.20.2',
        'PyQt5>=5.15.4',
        'Pillow>=8.1.2',
        'pywin32>=300',
        'pyautogui>=0.9.52'
    ],
    package_data={'holdem-machine-server': ['data/*.npy']},
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'holdem-machine-client = holdem_machine_client.command_line:main'
        ]
    },
    python_requires='>=3.9',
)