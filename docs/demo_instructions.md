### Frontend
```
cd client
docker build -t frontend-ds317:latest .
docker run -p 5173:5173 frontend-ds317:latest
```

### Backend
```
pip install -r requirements.txt
make db
make flask
```