import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.chat import router as chat_router
from excel.excel_connection import excel_conn

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main_server")

app = FastAPI(
    title="Excel AI MCP Backend Service",
    description="Backend service for AI-powered Excel workspace desktop application"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(chat_router)

@app.on_event("startup")
def startup_event():
    logger.info("Initializing Excel AI MCP Backend Service...")
    try:
        excel_conn.connect_excel()
        logger.info("Excel Connection Manager successfully initialized on startup.")
    except Exception as e:
        logger.error(f"Failed to initialize Excel Connection Manager on startup: {e}")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Shutting down Excel AI MCP Backend Service...")
    try:
        excel_conn.disconnect_excel()
        logger.info("Excel connection released and disconnected.")
    except Exception as e:
        logger.error(f"Error during Excel shutdown: {e}")
