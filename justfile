server:
	poetry run uvicorn plate_chain.server:app --reload

notebook:
	jupyter notebook