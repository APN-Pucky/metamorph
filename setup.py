import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    "termcolor",
    "deep_translator",
    "colorama",
    "pyyaml",
]


setuptools.setup(
    name="metamorph",
    setup_requires=['setuptools-git-versioning'],
    author="APN",
    author_email="APN-Pucky@no-reply.github.com",
    description="auto rewrite text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/APN-Pucky/metamorph",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    extras_require={
        'dev': [
            "build",
            "pytest",
            "pytest-cov",
            "pytest-profiling",
            "pytest-line-profiler-apn>=0.1.3",
            "jupyterlab",
            "pandas",
            "ipython",
        ],
        'doc': [
            "jupyter-sphinx",
            "sphinx_math_dollar",
            "pandoc",
            "sphinx",
            "sphinx-autoapi",
            "nbsphinx",
            "sphinx_rtd_theme",
            "numpydoc",
            "sphinx-autobuild",
        ]
    },
    version_config={
        "template": "{tag}",
        "dev_template": "{tag}.{ccount}",
        "dirty_template": "{tag}.{ccount}+dirty",
        "starting_version": "0.0.0",
        "version_callback": None,
        "version_file": None,
        "count_commits_from_version_file": False
    },
    #scripts=['metamorph'],
    entry_points = {
        'console_scripts': ['metamorph=metamorph.main:__main__'],
    },
    python_requires='>=3.6',
)
