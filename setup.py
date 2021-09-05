"""Package Setup File"""
import setuptools

with open("README.md") as readme_file:
    README = readme_file.read()

with open("HISTORY.md") as history_file:
    HISTORY = history_file.read()

REQUIREMENTS = ["pyyaml==5.4.1"]
TEST_REQUIREMENTS = ["pytest"]
EXTRAS_REQUIRE = {
    "dev": [
        "pylint",
        "black",
        "pre-commit",
    ] + TEST_REQUIREMENTS,
}

setuptools.setup(
    author="Lukas Koning",
    author_email="yaml-config@lukaskoning.nl",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    description="Easy configuration using YAML files.",
    install_requires=REQUIREMENTS,
    extras_require=EXTRAS_REQUIRE,
    long_description=README + "\n\n" + HISTORY,
    keywords="config, configuration, YAML",
    name="yaml_config",
    version="0.1.0",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    test_suite="tests",
    tests_require=TEST_REQUIREMENTS,
    url="https://github.com/LFKoning/yaml-config",
)
