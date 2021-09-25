eval "$(conda shell.bash hook)"
conda activate ser
cd /home/eason/Python/WEB/service/AI_Chatbot_platform/app
uvicorn app:app --port 13525 --workers 5 --proxy-headers --host 0.0.0.0
