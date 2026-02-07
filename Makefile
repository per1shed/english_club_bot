dev:
	uvicorn main:app --reload
prod:
	python main.py
cloudfl:
	cloudflared tunnel --url http://localhost:8000
	