import project
import pandas as pd
import pytest

data = pd.read_html('https://finance.yahoo.com/world-indices/')[0]
data = data[['Symbol', 'Name', 'Last Price', 'Change', '% Change']]
df = pd.DataFrame(data)
name_error = "this name has more than 31 characters and its gonna trigger ValueError"

def test_save_xlsl_data():
	with pytest.raises(ValueError):
		project.save_xlsl_data(df, name_error)

def test_validate_options():
	with pytest.raises(ValueError):
		project.validate_option(4, range(1, 4))
	assert project.validate_option(2, range(1, 3)) == 2
	assert project.validate_option(32, range(1, 37)) == 32

def test_validate_period():
	with pytest.raises(ValueError):
		project.validate_period("2 MO")
	with pytest.raises(ValueError):
		project.validate_period("2 D")
	assert project.validate_period("2 days") == "2d"
	assert project.validate_period("4 MONTH") == "4mo"
	assert project.validate_period("100 year") == "100y"

def test_play_sound():
	with pytest.raises(ValueError):
		project.play_sound("not a path")