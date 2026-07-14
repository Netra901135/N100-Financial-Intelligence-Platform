load:
	python src/etl/loader.py

test:
	pytest

clean:
	del /Q db\*.db
	del /Q output\*.csv