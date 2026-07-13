import sys
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.routers import (
    accounts,
    auth,
    books,
    budgets,
    categories,
    dashboard,
    gdrive,
    habits,
    notes,
    transactions,
    gcalendar,
    recovery,
    aicoach,
    public_preview,
    warborn_chat,
    governance_router,
    memory_router,
    action_admin_router,
    action_metrics_router,
)
from app.middleware.preview_rate_limit import PreviewRateLimitMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Validate environment configurations at startup
    from app.storage.config_validator import validate_config
    validate_config()

    # Run Alembic migrations via subprocess — fully isolated from asyncio, works with --reload
    import subprocess
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"MIGRATION ERROR:\n{result.stderr}", file=sys.stderr, flush=True)
    else:
        print("DEBUG: Migrations applied.", file=sys.stderr, flush=True)

    # Run seed synchronously via asyncio.to_thread (safe with --reload)
    import asyncio
    async def _seed():
        from seed import seed_sync
        await asyncio.to_thread(seed_sync)

    await _seed()
    print("DEBUG: Seeding complete.", file=sys.stderr, flush=True)

    yield
    # Shutdown
    from app.database import engine
    await engine.dispose()





app = FastAPI(
    title="WarBorn OS API",
    description="Single-user WarBorn operating system backend",
    version="0.50",
    lifespan=lifespan,
)

# CORS - include live domain alongside localhost
cors_origins = settings.cors_origins.split(",")
if "https://buildwithpnj.in" not in cors_origins:
    cors_origins.append("https://buildwithpnj.in")
if "https://www.buildwithpnj.in" not in cors_origins:
    cors_origins.append("https://www.buildwithpnj.in")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(PreviewRateLimitMiddleware)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"UNHANDLED 500 ERROR on {request.method} {request.url}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    return JSONResponse(status_code=500, content={"detail": str(exc)})

# Mount routers
app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(categories.router)
app.include_router(budgets.router)
app.include_router(dashboard.router)
app.include_router(gdrive.router)
app.include_router(notes.router)
app.include_router(books.router)
app.include_router(habits.router)
app.include_router(gcalendar.router)
app.include_router(recovery.router)
app.include_router(aicoach.router)
app.include_router(public_preview.router)
app.include_router(warborn_chat.router)
app.include_router(governance_router.router)
app.include_router(memory_router.router)
app.include_router(action_admin_router.router)
app.include_router(action_metrics_router.router)

# V16 & V17 routers
from app.routers.dead_letter_admin_router import router as dead_letter_admin_router
from app.routers.action_worker_metrics_router import router as action_worker_metrics_router
from app.routers.workflow_router import router as workflow_router

app.include_router(dead_letter_admin_router)
app.include_router(action_worker_metrics_router)
app.include_router(workflow_router)

# V19 control panel router
from app.routers.workflow_control_router import router as workflow_control_router
app.include_router(workflow_control_router)

# V20 workflow diagnostics router
from app.routers.workflow_diagnostic_router import router as workflow_diagnostic_router
app.include_router(workflow_diagnostic_router)

# V21 workflow graph visualizer router
from app.routers.workflow_graph_router import router as workflow_graph_router
app.include_router(workflow_graph_router)

# V24 delegation policy router
from app.routers.delegation_policy_router import router as delegation_policy_router
app.include_router(delegation_policy_router)

# V25 multimodal ingestion router
from app.routers.multimodal_router import router as multimodal_router
app.include_router(multimodal_router)

# V26 Global Copilot router
from app.routers.copilot_router import router as copilot_router
app.include_router(copilot_router)

# V27 Multimodal Governance router
from app.routers.multimodal_governance_router import router as multimodal_governance_router
app.include_router(multimodal_governance_router)

# V28 Long-Horizon Goals router
from app.routers.objective_router import router as objective_router
app.include_router(objective_router)

# V29 Simulation router
from app.routers.simulation_router import router as simulation_router
app.include_router(simulation_router)

# V30 Memory Compaction router
from app.routers.context_optimization_router import router as context_optimization_router
app.include_router(context_optimization_router)

# V31 Notification router
from app.routers.notification_router import router as notification_router
app.include_router(notification_router)

# V33 Operating Thread router
from app.routers.operating_thread_router import router as operating_thread_router
app.include_router(operating_thread_router)

# V34 Governance router (Already mounted in the main block)
# from app.routers.governance_router import router as governance_router
# app.include_router(governance_router)

# V35 Governance Sync router
from app.routers.governance_sync_router import router as governance_sync_router
app.include_router(governance_sync_router)

# V36 Release Control router
from app.routers.release_control_router import router as release_control_router
app.include_router(release_control_router)

# V37 Distributed Telemetry router
from app.routers.telemetry_router import router as telemetry_router
app.include_router(telemetry_router)

# V37 Anomaly router
from app.routers.anomaly_router import router as anomaly_router
app.include_router(anomaly_router)

# V38 Resilience router
from app.routers.resilience_router import router as resilience_router
app.include_router(resilience_router)

# V39 Ops Analytics router
from app.routers.ops_analytics_router import router as ops_analytics_router
app.include_router(ops_analytics_router)

# RAG Knowledge router
from app.routers.knowledge_router import router as knowledge_router
app.include_router(knowledge_router)

# RAG Retrieval router
from app.routers.retrieval_router import router as retrieval_router
app.include_router(retrieval_router)

# RAG Retrieval Eval router
from app.routers.retrieval_eval_router import router as retrieval_eval_router
app.include_router(retrieval_eval_router)

# V18 WebSocket Endpoint
from fastapi import WebSocket, WebSocketDisconnect
from app.realtime.websocket_manager import WebSocketManager

@app.websocket("/api/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await WebSocketManager.connect(websocket, user_id, "approved_user")
    try:
        while True:
            # Listen to keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        WebSocketManager.disconnect(websocket)
from app.storage.routes import router as storage_router
app.include_router(storage_router)

# Local LLM diagnostics
from app.routers.llm_diagnostics_router import router as llm_diagnostics_router
app.include_router(llm_diagnostics_router)

@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.50"}

