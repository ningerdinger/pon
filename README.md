# pon

tutorial to package this https://packaging.python.org/en/latest/tutorials/packaging-projects/

run this

python3 -m pip install --upgrade build

run this from the toml directory

python3 -m build

install twine

python3 -m pip install --upgrade twine

Make sure that you have a pypi account and token

run this to upload to pypi

python3 -m twine upload --repository testpypi dist/*

then just install from pypi and run it
