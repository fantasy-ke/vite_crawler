from setuptools import setup, find_packages

setup(
    name="vite_crawler",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.0',
        'lxml>=4.9.0',
        'pathvalidate>=3.0.0',
    ],
    entry_points={
        'console_scripts': [
            'vite-crawler=src.main:main',
        ],
    },
    author="fantasy-ke",
    author_email="fantasyke@qq.com",
    description="A web crawler for downloading website content",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fantasy-ke/vite_crawler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
) 