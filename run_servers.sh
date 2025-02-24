cd ./backend
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload &
cd ..

cd ./frontend
npm start &
cd ..