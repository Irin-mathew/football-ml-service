# # """
# # FastAPI Performance Enhanced Server - IMPORT FIXED
# # """

# # from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
# # from fastapi.responses import JSONResponse, StreamingResponse, FileResponse, HTMLResponse
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.staticfiles import StaticFiles
# # import uvicorn
# # import os
# # import uuid
# # import shutil
# # from pathlib import Path
# # from datetime import datetime
# # import cv2
# # import json
# # import asyncio
# # from typing import Optional

# # # Import your analyzer
# # from football_analyzer_fixed import FootballPerformanceAnalyzer

# # app = FastAPI(title="Football Performance Analyzer API", version="1.0.0")

# # # CORS
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Configuration
# # UPLOAD_FOLDER = Path("uploads")
# # OUTPUT_FOLDER = Path("outputs")
# # STATIC_FOLDER = Path("static")

# # for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, STATIC_FOLDER]:
# #     folder.mkdir(exist_ok=True)

# # # Mount static files
# # try:
# #     app.mount("/static", StaticFiles(directory=str(STATIC_FOLDER)), name="static")
# #     app.mount("/outputs", StaticFiles(directory=str(OUTPUT_FOLDER)), name="outputs")
# # except Exception as e:
# #     print(f"Warning: Could not mount static files: {e}")

# # # Store active sessions
# # sessions = {}
# # analyzers = {}

# # # Helper functions
# # def allowed_file(filename: str) -> bool:
# #     ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
# #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # @app.get("/")
# # async def root():
# #     """API information"""
# #     return HTMLResponse("""
# #     <!DOCTYPE html>
# #     <html>
# #     <head>
# #         <title>Football Performance Analyzer API</title>
# #         <style>
# #             body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
# #             h1 { color: #2c3e50; }
# #             .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }
# #             .method { display: inline-block; padding: 5px 10px; border-radius: 3px; font-weight: bold; }
# #             .get { background: #28a745; color: white; }
# #             .post { background: #007bff; color: white; }
# #             code { background: #e9ecef; padding: 2px 6px; border-radius: 3px; }
# #         </style>
# #     </head>
# #     <body>
# #         <h1>⚽ Football Performance Analyzer API</h1>
# #         <p>FastAPI server with FIXED imports and occlusion handling</p>
        
# #         <h2>Available Endpoints:</h2>
        
# #         <div class="endpoint">
# #             <span class="method post">POST</span>
# #             <strong>/api/upload</strong>
# #             <p>Upload a video file for analysis</p>
# #             <code>curl -X POST -F "video=@match.mp4" http://localhost:8000/api/upload</code>
# #         </div>
        
# #         <div class="endpoint">
# #             <span class="method post">POST</span>
# #             <strong>/api/process</strong>
# #             <p>Process uploaded video</p>
# #             <code>curl -X POST -H "Content-Type: application/json" -d '{"session_id":"xxx","video_path":"uploads/xxx.mp4"}' http://localhost:8000/api/process</code>
# #         </div>
        
# #         <div class="endpoint">
# #             <span class="method get">GET</span>
# #             <strong>/api/player/{id}/stats</strong>
# #             <p>Get player statistics</p>
# #             <code>curl http://localhost:8000/api/player/5/stats?session_id=xxx</code>
# #         </div>
        
# #         <div class="endpoint">
# #             <span class="method get">GET</span>
# #             <strong>/api/player/{id}/card</strong>
# #             <p>Get player performance card</p>
# #             <code>curl http://localhost:8000/api/player/5/card?session_id=xxx</code>
# #         </div>
        
# #         <div class="endpoint">
# #             <span class="method get">GET</span>
# #             <strong>/api/player/{id}/heatmap</strong>
# #             <p>Get player heatmap</p>
# #             <code>curl http://localhost:8000/api/player/5/heatmap?session_id=xxx</code>
# #         </div>
        
# #         <div class="endpoint">
# #             <span class="method get">GET</span>
# #             <strong>/api/sessions</strong>
# #             <p>List active sessions</p>
# #             <code>curl http://localhost:8000/api/sessions</code>
# #         </div>
        
# #         <div class="endpoint">
# #             <span class="method get">GET</span>
# #             <strong>/docs</strong>
# #             <p>Interactive API documentation (Swagger UI)</p>
# #         </div>
        
# #         <p style="margin-top: 30px; color: #6c757d;">
# #             Version 1.0.0 | Fixed imports | Occlusion handling enabled
# #         </p>
# #     </body>
# #     </html>
# #     """)

# # @app.get("/api/health")
# # async def health_check():
# #     """Health check endpoint"""
# #     return JSONResponse({
# #         "status": "healthy",
# #         "service": "Football Performance Analyzer",
# #         "version": "1.0.0-fixed",
# #         "timestamp": datetime.now().isoformat(),
# #         "active_sessions": len(sessions)
# #     })

# # @app.post("/api/upload")
# # async def upload_video(video: UploadFile = File(...)):
# #     """Upload video file"""
# #     try:
# #         # Validate file
# #         if not allowed_file(video.filename):
# #             raise HTTPException(
# #                 status_code=400,
# #                 detail="Invalid file type. Allowed: mp4, avi, mov, mkv"
# #             )
        
# #         # Create session
# #         session_id = str(uuid.uuid4())
# #         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
# #         filename = f"{session_id}_{timestamp}_{video.filename}"
# #         video_path = UPLOAD_FOLDER / filename
        
# #         # Save file
# #         with open(video_path, "wb") as buffer:
# #             shutil.copyfileobj(video.file, buffer)
        
# #         # Get video info
# #         cap = cv2.VideoCapture(str(video_path))
# #         fps = cap.get(cv2.CAP_PROP_FPS)
# #         total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# #         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# #         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# #         duration = total_frames / fps if fps > 0 else 0
# #         cap.release()
        
# #         # Store session info
# #         sessions[session_id] = {
# #             "video_path": str(video_path),
# #             "filename": filename,
# #             "upload_time": datetime.now().isoformat(),
# #             "status": "uploaded"
# #         }
        
# #         return JSONResponse({
# #             "session_id": session_id,
# #             "video_path": str(video_path),
# #             "filename": filename,
# #             "video_info": {
# #                 "fps": fps,
# #                 "total_frames": total_frames,
# #                 "width": width,
# #                 "height": height,
# #                 "duration_seconds": duration
# #             },
# #             "message": "Upload successful"
# #         })
        
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))

# # @app.post("/api/process")
# # async def process_video(
# #     session_id: str = Form(...),
# #     video_path: str = Form(...),
# #     use_cache: bool = Form(True)
# # ):
# #     """Process video"""
# #     try:
# #         # Validate session
# #         if session_id not in sessions:
# #             raise HTTPException(status_code=404, detail="Session not found")
        
# #         # Validate video exists
# #         if not Path(video_path).exists():
# #             raise HTTPException(status_code=404, detail="Video file not found")
        
# #         # Create or get analyzer
# #         if session_id not in analyzers:
# #             analyzers[session_id] = FootballPerformanceAnalyzer()
        
# #         analyzer = analyzers[session_id]
        
# #         # Process video
# #         print(f"\n🎬 Processing video for session {session_id}...")
# #         player_stats, player_images = analyzer.process_video(
# #             video_path,
# #             use_stubs=use_cache
# #         )
        
# #         # Update session
# #         sessions[session_id]["status"] = "processed"
# #         sessions[session_id]["player_count"] = len(player_stats)
# #         sessions[session_id]["process_time"] = datetime.now().isoformat()
        
# #         # Prepare response
# #         players = []
# #         for player_id, stats in player_stats.items():
# #             players.append({
# #                 "player_id": int(player_id),
# #                 "stats": stats,
# #                 "has_image": player_id in player_images
# #             })
        
# #         return JSONResponse({
# #             "session_id": session_id,
# #             "total_players": len(players),
# #             "players": players,
# #             "message": "Processing complete"
# #         })
        
# #     except Exception as e:
# #         import traceback
# #         traceback.print_exc()
# #         raise HTTPException(status_code=500, detail=str(e))

# # @app.get("/api/player/{player_id}/stats")
# # async def get_player_stats(player_id: int, session_id: str):
# #     """Get player statistics"""
# #     try:
# #         if session_id not in analyzers:
# #             raise HTTPException(status_code=404, detail="Session not found")
        
# #         analyzer = analyzers[session_id]
        
# #         if player_id not in analyzer.player_stats:
# #             raise HTTPException(status_code=404, detail="Player not found")
        
# #         return JSONResponse({
# #             "player_id": player_id,
# #             "stats": analyzer.player_stats[player_id],
# #             "has_image": player_id in analyzer.player_images
# #         })
        
# #     except HTTPException:
# #         raise
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))

# # @app.get("/api/player/{player_id}/card")
# # async def get_player_card(player_id: int, session_id: str, format: str = "image"):
# #     """Get player card"""
# #     try:
# #         if session_id not in analyzers:
# #             raise HTTPException(status_code=404, detail="Session not found")
        
# #         analyzer = analyzers[session_id]
        
# #         if player_id not in analyzer.player_stats:
# #             raise HTTPException(status_code=404, detail="Player not found")
        
# #         if format == "json":
# #             return JSONResponse({
# #                 "player_id": player_id,
# #                 "stats": analyzer.player_stats[player_id]
# #             })
        
# #         # Generate card
# #         fig = analyzer.generate_player_card(player_id)
# #         if fig is None:
# #             raise HTTPException(status_code=500, detail="Cannot generate card")
        
# #         # Save to file
# #         output_path = OUTPUT_FOLDER / f"player_{player_id}_card.png"
# #         fig.savefig(output_path, dpi=150, bbox_inches='tight')
        
# #         import matplotlib.pyplot as plt
# #         plt.close(fig)
        
# #         # Return file
# #         return FileResponse(
# #             output_path,
# #             media_type="image/png",
# #             filename=f"player_{player_id}_card.png"
# #         )
        
# #     except HTTPException:
# #         raise
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))

# # @app.get("/api/player/{player_id}/heatmap")
# # async def get_player_heatmap(player_id: int, session_id: str, bins: int = 60):
# #     """Get player heatmap"""
# #     try:
# #         if session_id not in analyzers:
# #             raise HTTPException(status_code=404, detail="Session not found")
        
# #         analyzer = analyzers[session_id]
        
# #         if player_id not in analyzer.player_stats:
# #             raise HTTPException(status_code=404, detail="Player not found")
        
# #         # Generate heatmap
# #         fig = analyzer.generate_heatmap(player_id, bins=bins)
# #         if fig is None:
# #             raise HTTPException(status_code=500, detail="Cannot generate heatmap")
        
# #         # Save to file
# #         output_path = OUTPUT_FOLDER / f"player_{player_id}_heatmap.png"
# #         fig.savefig(output_path, dpi=150, bbox_inches='tight')
        
# #         import matplotlib.pyplot as plt
# #         plt.close(fig)
        
# #         # Return file
# #         return FileResponse(
# #             output_path,
# #             media_type="image/png",
# #             filename=f"player_{player_id}_heatmap.png"
# #         )
        
# #     except HTTPException:
# #         raise
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))

# # @app.get("/api/player/{player_id}/recovery")
# # async def get_recovery_plan(player_id: int, session_id: str):
# #     """Get recovery plan"""
# #     try:
# #         if session_id not in analyzers:
# #             raise HTTPException(status_code=404, detail="Session not found")
        
# #         analyzer = analyzers[session_id]
        
# #         if player_id not in analyzer.player_stats:
# #             raise HTTPException(status_code=404, detail="Player not found")
        
# #         # Generate recovery plan
# #         result = analyzer.generate_recovery_plan(player_id)
# #         if result is None:
# #             raise HTTPException(status_code=500, detail="Cannot generate recovery plan")
        
# #         return JSONResponse({
# #             "player_id": player_id,
# #             "injury_prediction": result["injury_prediction"],
# #             "recovery_plan": result["recovery_plan"],
# #             "text_report": result.get("text_report", ""),
# #             "recovery_card_path": result.get("recovery_card_path", "")
# #         })
        
# #     except HTTPException:
# #         raise
# #     except Exception as e:
# #         import traceback
# #         traceback.print_exc()
# #         raise HTTPException(status_code=500, detail=str(e))

# # @app.get("/api/sessions")
# # async def list_sessions():
# #     """List active sessions"""
# #     return JSONResponse({
# #         "active_sessions": list(sessions.keys()),
# #         "total_sessions": len(sessions),
# #         "sessions": sessions
# #     })

# # @app.delete("/api/session/{session_id}")
# # async def delete_session(session_id: str):
# #     """Delete session and cleanup"""
# #     try:
# #         if session_id in sessions:
# #             # Delete video file
# #             video_path = sessions[session_id].get("video_path")
# #             if video_path and Path(video_path).exists():
# #                 Path(video_path).unlink()
            
# #             # Remove from sessions
# #             del sessions[session_id]
            
# #             # Remove analyzer
# #             if session_id in analyzers:
# #                 del analyzers[session_id]
            
# #             return JSONResponse({
# #                 "message": "Session deleted",
# #                 "session_id": session_id
# #             })
# #         else:
# #             raise HTTPException(status_code=404, detail="Session not found")
# #     except HTTPException:
# #         raise
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))

# # @app.get("/api/export/{session_id}")
# # async def export_session(session_id: str):
# #     """Export session data to JSON"""
# #     try:
# #         if session_id not in analyzers:
# #             raise HTTPException(status_code=404, detail="Session not found")
        
# #         analyzer = analyzers[session_id]
        
# #         output_filename = f"analysis_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
# #         output_path = OUTPUT_FOLDER / output_filename
        
# #         export_data = analyzer.export_to_json(str(output_path))
        
# #         return FileResponse(
# #             output_path,
# #             media_type="application/json",
# #             filename=output_filename
# #         )
        
# #     except HTTPException:
# #         raise
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))

# # if __name__ == "__main__":
# #     print("=" * 70)
# #     print("⚽ FOOTBALL ANALYZER - FASTAPI SERVER (FIXED)")
# #     print("=" * 70)
# #     print("\n✅ All imports fixed")
# #     print("✅ Occlusion handling enabled")
# #     print("✅ Ready for production\n")
# #     print("=" * 70)
# #     print(f"\n📁 Folders:")
# #     print(f"   Upload: {UPLOAD_FOLDER}")
# #     print(f"   Output: {OUTPUT_FOLDER}")
# #     print(f"   Static: {STATIC_FOLDER}\n")
# #     print("=" * 70)
# #     print("\n🚀 Starting server...")
# #     print("📖 API docs: http://localhost:8000/docs")
# #     print("🏠 Home: http://localhost:8000")
# #     print("💡 Press Ctrl+C to stop\n")
    
# #     uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

# """
# ENHANCED FastAPI Server with Frame Streaming
# - Real-time frame streaming via Server-Sent Events (SSE)
# - WebSocket support for progress updates
# - Improved error handling
# """

# from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
# from fastapi.responses import JSONResponse, StreamingResponse, FileResponse, HTMLResponse
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# import uvicorn
# import os
# import uuid
# import shutil
# from pathlib import Path
# from datetime import datetime
# import cv2
# import json
# import asyncio
# from typing import Optional
# import queue
# import threading
# import base64
# import time

# # Import enhanced analyzer
# from football_analyzer_fixed import FootballPerformanceAnalyzer

# app = FastAPI(title="Football Performance Analyzer API - Enhanced", version="2.0.0")

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Configuration
# UPLOAD_FOLDER = Path("uploads")
# OUTPUT_FOLDER = Path("outputs")
# STATIC_FOLDER = Path("static")

# for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, STATIC_FOLDER]:
#     folder.mkdir(exist_ok=True)

# # Mount static files
# try:
#     app.mount("/static", StaticFiles(directory=str(STATIC_FOLDER)), name="static")
#     app.mount("/outputs", StaticFiles(directory=str(OUTPUT_FOLDER)), name="outputs")
# except Exception as e:
#     print(f"Warning: Could not mount static files: {e}")

# # Store active sessions
# sessions = {}
# analyzers = {}
# frame_queues = {}  # For frame streaming
# processing_threads = {}

# # Helper functions
# def allowed_file(filename: str) -> bool:
#     ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def encode_frame_to_base64(frame):
#     """Encode frame to base64 JPEG"""
#     try:
#         # Resize for faster transmission
#         h, w = frame.shape[:2]
#         if w > 1280:
#             scale = 1280 / w
#             frame = cv2.resize(frame, (int(w*scale), int(h*scale)))
        
#         _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
#         return base64.b64encode(buffer).decode('utf-8')
#     except Exception as e:
#         print(f"Frame encode error: {e}")
#         return None

# @app.get("/")
# async def root():
#     """API information"""
#     return HTMLResponse("""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Football Performance Analyzer API - Enhanced</title>
#         <style>
#             body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; }
#             h1 { color: #2c3e50; }
#             .feature { background: #e8f5e9; padding: 15px; margin: 10px 0; border-left: 4px solid #4caf50; }
#             .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }
#             .method { display: inline-block; padding: 5px 10px; border-radius: 3px; font-weight: bold; }
#             .get { background: #28a745; color: white; }
#             .post { background: #007bff; color: white; }
#             code { background: #e9ecef; padding: 2px 6px; border-radius: 3px; }
#             .new { background: #ffc107; color: #000; padding: 2px 8px; border-radius: 3px; font-size: 0.8em; }
#         </style>
#     </head>
#     <body>
#         <h1>⚽ Football Performance Analyzer API v2.0 (Enhanced)</h1>
#         <p>FastAPI server with streaming, WebSockets, and improved tracking</p>
        
#         <h2>🚀 New Features:</h2>
#         <div class="feature">
#             <strong>📡 Frame Streaming:</strong> Real-time annotated frames via SSE
#         </div>
#         <div class="feature">
#             <strong>🔌 WebSocket Support:</strong> Live progress updates
#         </div>
#         <div class="feature">
#             <strong>🎯 Better Tracking:</strong> 8-second buffer, aggressive detection (conf=0.08)
#         </div>
#         <div class="feature">
#             <strong>📊 Quality Monitoring:</strong> Track consistency throughout video
#         </div>
        
#         <h2>Available Endpoints:</h2>
        
#         <div class="endpoint">
#             <span class="method post">POST</span>
#             <strong>/api/upload</strong>
#             <p>Upload a video file for analysis</p>
#         </div>
        
#         <div class="endpoint">
#             <span class="method post">POST</span>
#             <strong>/api/process</strong> <span class="new">ENHANCED</span>
#             <p>Process uploaded video with streaming support</p>
#         </div>
        
#         <div class="endpoint">
#             <span class="method get">GET</span>
#             <strong>/api/stream/{session_id}</strong> <span class="new">NEW</span>
#             <p>Stream annotated frames (Server-Sent Events)</p>
#         </div>
        
#         <div class="endpoint">
#             <span class="method get">GET</span>
#             <strong>/ws/progress/{session_id}</strong> <span class="new">NEW</span>
#             <p>WebSocket for real-time progress updates</p>
#         </div>
        
#         <div class="endpoint">
#             <span class="method get">GET</span>
#             <strong>/api/player/{id}/stats</strong>
#             <p>Get player statistics</p>
#         </div>
        
#         <div class="endpoint">
#             <span class="method get">GET</span>
#             <strong>/api/player/{id}/card</strong>
#             <p>Get player performance card (PNG)</p>
#         </div>
        
#         <div class="endpoint">
#             <span class="method get">GET</span>
#             <strong>/api/player/{id}/heatmap</strong>
#             <p>Get player movement heatmap (PNG)</p>
#         </div>
        
#         <div class="endpoint">
#             <span class="method get">GET</span>
#             <strong>/api/sessions</strong>
#             <p>List active sessions</p>
#         </div>
        
#         <p style="margin-top: 30px; color: #6c757d;">
#             Version 2.0.0 | Enhanced tracking | Frame streaming | WebSocket support
#         </p>
#     </body>
#     </html>
#     """)

# @app.get("/api/health")
# async def health_check():
#     """Health check endpoint"""
#     return JSONResponse({
#         "status": "healthy",
#         "service": "Football Performance Analyzer Enhanced",
#         "version": "2.0.0",
#         "features": ["streaming", "websocket", "aggressive_tracking"],
#         "timestamp": datetime.now().isoformat(),
#         "active_sessions": len(sessions),
#         "processing": len(processing_threads)
#     })

# @app.post("/api/upload")
# async def upload_video(video: UploadFile = File(...)):
#     """Upload video file"""
#     try:
#         # Validate file
#         if not allowed_file(video.filename):
#             raise HTTPException(
#                 status_code=400,
#                 detail="Invalid file type. Allowed: mp4, avi, mov, mkv"
#             )
        
#         # Create session
#         session_id = str(uuid.uuid4())
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         filename = f"{session_id}_{timestamp}_{video.filename}"
#         video_path = UPLOAD_FOLDER / filename
        
#         # Save file
#         with open(video_path, "wb") as buffer:
#             shutil.copyfileobj(video.file, buffer)
        
#         # Get video info
#         cap = cv2.VideoCapture(str(video_path))
#         fps = cap.get(cv2.CAP_PROP_FPS)
#         total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         duration = total_frames / fps if fps > 0 else 0
#         cap.release()
        
#         # Store session info
#         sessions[session_id] = {
#             "video_path": str(video_path),
#             "filename": filename,
#             "upload_time": datetime.now().isoformat(),
#             "status": "uploaded"
#         }
        
#         return JSONResponse({
#             "session_id": session_id,
#             "video_path": str(video_path),
#             "filename": filename,
#             "video_info": {
#                 "fps": fps,
#                 "total_frames": total_frames,
#                 "width": width,
#                 "height": height,
#                 "duration_seconds": duration
#             },
#             "message": "Upload successful"
#         })
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/api/process")
# async def process_video(
#     background_tasks: BackgroundTasks,
#     session_id: str = Form(...),
#     video_path: str = Form(...),
#     use_cache: bool = Form(True),
#     enable_streaming: bool = Form(False)
# ):
#     """Process video with optional frame streaming"""
#     try:
#         # Validate session
#         if session_id not in sessions:
#             raise HTTPException(status_code=404, detail="Session not found")
        
#         # Validate video exists
#         if not Path(video_path).exists():
#             raise HTTPException(status_code=404, detail="Video file not found")
        
#         # Create or get analyzer
#         if session_id not in analyzers:
#             analyzers[session_id] = FootballPerformanceAnalyzer()
        
#         # Create frame queue if streaming enabled
#         if enable_streaming:
#             frame_queues[session_id] = queue.Queue(maxsize=10)
        
#         # Process in background
#         def process_task():
#             try:
#                 analyzer = analyzers[session_id]
                
#                 # Frame callback for streaming
#                 def frame_callback(frame):
#                     if enable_streaming and session_id in frame_queues:
#                         try:
#                             # Non-blocking put with timeout
#                             frame_queues[session_id].put(frame, block=False)
#                         except queue.Full:
#                             # Skip frame if queue full
#                             pass
                
#                 print(f"\n🎬 Processing video for session {session_id}...")
#                 player_stats, player_images = analyzer.process_video(
#                     video_path,
#                     use_stubs=use_cache,
#                     frame_callback=frame_callback if enable_streaming else None
#                 )
                
#                 # Signal end of stream
#                 if enable_streaming and session_id in frame_queues:
#                     frame_queues[session_id].put(None)  # Sentinel
                
#                 # Update session
#                 sessions[session_id]["status"] = "processed"
#                 sessions[session_id]["player_count"] = len(player_stats)
#                 sessions[session_id]["process_time"] = datetime.now().isoformat()
                
#                 print(f"✅ Session {session_id} complete: {len(player_stats)} players")
                
#             except Exception as e:
#                 print(f"❌ Processing error for {session_id}: {e}")
#                 import traceback
#                 traceback.print_exc()
#                 sessions[session_id]["status"] = "error"
#                 sessions[session_id]["error"] = str(e)
#             finally:
#                 # Cleanup
#                 if session_id in processing_threads:
#                     del processing_threads[session_id]
        
#         # Start processing thread
#         thread = threading.Thread(target=process_task, daemon=True)
#         thread.start()
#         processing_threads[session_id] = thread
        
#         sessions[session_id]["status"] = "processing"
        
#         return JSONResponse({
#             "session_id": session_id,
#             "status": "processing",
#             "streaming_enabled": enable_streaming,
#             "stream_url": f"/api/stream/{session_id}" if enable_streaming else None,
#             "message": "Processing started"
#         })
        
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/stream/{session_id}")
# async def stream_frames(session_id: str):
#     """Stream annotated frames via Server-Sent Events"""
#     if session_id not in frame_queues:
#         raise HTTPException(status_code=404, detail="No stream available for this session")
    
#     async def generate():
#         fq = frame_queues[session_id]
#         frame_count = 0
        
#         try:
#             while True:
#                 try:
#                     # Get frame from queue (blocking with timeout)
#                     frame = fq.get(timeout=30)
                    
#                     # Sentinel value means end of stream
#                     if frame is None:
#                         yield f"data: {json.dumps({'type': 'end'})}\n\n"
#                         break
                    
#                     # Encode to base64
#                     frame_b64 = encode_frame_to_base64(frame)
#                     if frame_b64:
#                         frame_count += 1
#                         data = {
#                             'type': 'frame',
#                             'frame_number': frame_count,
#                             'data': frame_b64
#                         }
#                         yield f"data: {json.dumps(data)}\n\n"
                    
#                     await asyncio.sleep(0.01)  # Small delay to prevent overwhelming
                    
#                 except queue.Empty:
#                     # Send keepalive
#                     yield f"data: {json.dumps({'type': 'keepalive'})}\n\n"
                    
#         except Exception as e:
#             print(f"Stream error: {e}")
#             yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
#         finally:
#             # Cleanup
#             if session_id in frame_queues:
#                 del frame_queues[session_id]
    
#     return StreamingResponse(
#         generate(),
#         media_type="text/event-stream",
#         headers={
#             "Cache-Control": "no-cache",
#             "Connection": "keep-alive",
#         }
#     )

# @app.get("/api/status/{session_id}")
# async def get_status(session_id: str):
#     """Get processing status"""
#     if session_id not in sessions:
#         raise HTTPException(status_code=404, detail="Session not found")
    
#     session = sessions[session_id]
#     status = {
#         "session_id": session_id,
#         "status": session.get("status", "unknown"),
#         "filename": session.get("filename"),
#         "is_processing": session_id in processing_threads
#     }
    
#     if session.get("status") == "processed":
#         if session_id in analyzers:
#             status["player_count"] = len(analyzers[session_id].player_stats)
    
#     if session.get("status") == "error":
#         status["error"] = session.get("error")
    
#     return JSONResponse(status)

# @app.get("/api/player/{player_id}/stats")
# async def get_player_stats(player_id: int, session_id: str):
#     """Get player statistics"""
#     try:
#         if session_id not in analyzers:
#             raise HTTPException(status_code=404, detail="Session not found")
        
#         analyzer = analyzers[session_id]
        
#         if player_id not in analyzer.player_stats:
#             raise HTTPException(status_code=404, detail="Player not found")
        
#         return JSONResponse({
#             "player_id": player_id,
#             "stats": analyzer.player_stats[player_id],
#             "has_image": player_id in analyzer.player_images
#         })
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/player/{player_id}/card")
# async def get_player_card(player_id: int, session_id: str, format: str = "image"):
#     """Get player card"""
#     try:
#         if session_id not in analyzers:
#             raise HTTPException(status_code=404, detail="Session not found")
        
#         analyzer = analyzers[session_id]
        
#         if player_id not in analyzer.player_stats:
#             raise HTTPException(status_code=404, detail="Player not found")
        
#         if format == "json":
#             return JSONResponse({
#                 "player_id": player_id,
#                 "stats": analyzer.player_stats[player_id]
#             })
        
#         # Generate card
#         fig = analyzer.generate_player_card(player_id)
#         if fig is None:
#             raise HTTPException(status_code=500, detail="Cannot generate card")
        
#         # Save to file
#         output_path = OUTPUT_FOLDER / f"player_{player_id}_card_{session_id}.png"
#         fig.savefig(output_path, dpi=150, bbox_inches='tight')
        
#         import matplotlib.pyplot as plt
#         plt.close(fig)
        
#         # Return file
#         return FileResponse(
#             output_path,
#             media_type="image/png",
#             filename=f"player_{player_id}_card.png"
#         )
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/player/{player_id}/heatmap")
# async def get_player_heatmap(player_id: int, session_id: str, bins: int = 60):
#     """Get player heatmap"""
#     try:
#         if session_id not in analyzers:
#             raise HTTPException(status_code=404, detail="Session not found")
        
#         analyzer = analyzers[session_id]
        
#         if player_id not in analyzer.player_stats:
#             raise HTTPException(status_code=404, detail="Player not found")
        
#         # Generate heatmap
#         fig = analyzer.generate_heatmap(player_id, bins=bins)
#         if fig is None:
#             raise HTTPException(status_code=500, detail="Cannot generate heatmap")
        
#         # Save to file
#         output_path = OUTPUT_FOLDER / f"player_{player_id}_heatmap_{session_id}.png"
#         fig.savefig(output_path, dpi=150, bbox_inches='tight')
        
#         import matplotlib.pyplot as plt
#         plt.close(fig)
        
#         # Return file
#         return FileResponse(
#             output_path,
#             media_type="image/png",
#             filename=f"player_{player_id}_heatmap.png"
#         )
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/player/{player_id}/recovery")
# async def get_recovery_plan(player_id: int, session_id: str):
#     """Get recovery plan"""
#     try:
#         if session_id not in analyzers:
#             raise HTTPException(status_code=404, detail="Session not found")
        
#         analyzer = analyzers[session_id]
        
#         if player_id not in analyzer.player_stats:
#             raise HTTPException(status_code=404, detail="Player not found")
        
#         # Generate recovery plan
#         result = analyzer.generate_recovery_plan(player_id)
#         if result is None:
#             raise HTTPException(status_code=500, detail="Cannot generate recovery plan")
        
#         return JSONResponse({
#             "player_id": player_id,
#             "injury_prediction": result["injury_prediction"],
#             "recovery_plan": result["recovery_plan"],
#             "text_report": result.get("text_report", ""),
#             "recovery_card_path": result.get("recovery_card_path", "")
#         })
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/sessions")
# async def list_sessions():
#     """List active sessions"""
#     session_list = []
#     for sid, session in sessions.items():
#         session_list.append({
#             "session_id": sid,
#             "filename": session.get("filename"),
#             "status": session.get("status"),
#             "upload_time": session.get("upload_time"),
#             "is_processing": sid in processing_threads,
#             "has_analyzer": sid in analyzers
#         })
    
#     return JSONResponse({
#         "active_sessions": len(sessions),
#         "processing": len(processing_threads),
#         "sessions": session_list
#     })

# @app.delete("/api/session/{session_id}")
# async def delete_session(session_id: str):
#     """Delete session and cleanup"""
#     try:
#         if session_id in sessions:
#             # Delete video file
#             video_path = sessions[session_id].get("video_path")
#             if video_path and Path(video_path).exists():
#                 Path(video_path).unlink()
            
#             # Remove from sessions
#             del sessions[session_id]
            
#             # Remove analyzer
#             if session_id in analyzers:
#                 del analyzers[session_id]
            
#             # Remove frame queue
#             if session_id in frame_queues:
#                 del frame_queues[session_id]
            
#             return JSONResponse({
#                 "message": "Session deleted",
#                 "session_id": session_id
#             })
#         else:
#             raise HTTPException(status_code=404, detail="Session not found")
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/export/{session_id}")
# async def export_session(session_id: str):
#     """Export session data to JSON"""
#     try:
#         if session_id not in analyzers:
#             raise HTTPException(status_code=404, detail="Session not found")
        
#         analyzer = analyzers[session_id]
        
#         output_filename = f"analysis_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
#         output_path = OUTPUT_FOLDER / output_filename
        
#         export_data = analyzer.export_to_json(str(output_path))
        
#         return FileResponse(
#             output_path,
#             media_type="application/json",
#             filename=output_filename
#         )
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     print("=" * 80)
#     print("⚽ FOOTBALL ANALYZER - ENHANCED FASTAPI SERVER v2.0")
#     print("=" * 80)
#     print("\n✅ Features:")
#     print("   📡 Real-time frame streaming (SSE)")
#     print("   🎯 Aggressive tracking (8-second buffer, conf=0.08)")
#     print("   📊 Quality monitoring throughout video")
#     print("   🔧 Improved occlusion handling")
#     print("\n=" * 80)
#     print(f"\n📁 Folders:")
#     print(f"   Upload: {UPLOAD_FOLDER}")
#     print(f"   Output: {OUTPUT_FOLDER}")
#     print(f"   Static: {STATIC_FOLDER}\n")
#     print("=" * 80)
#     print("\n🚀 Starting server...")
#     print("📖 API docs: http://localhost:8000/docs")
#     print("🏠 Home: http://localhost:8000")
#     print("💡 Press Ctrl+C to stop\n")
    
#     uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

"""
ENHANCED FastAPI Server with Frame Streaming
- Real-time frame streaming via Server-Sent Events (SSE)
- WebSocket support for progress updates
- Improved error handling
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import uuid
import shutil
from pathlib import Path
from datetime import datetime
import cv2
import json
import asyncio
from typing import Optional
import queue
import threading
import base64
import time

# Import ultimate analyzer with referee fix
from football_analyzer_fixed import FootballPerformanceAnalyzer

app = FastAPI(title="Football Performance Analyzer API - Enhanced", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_FOLDER = Path("uploads")
OUTPUT_FOLDER = Path("outputs")
STATIC_FOLDER = Path("static")

for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, STATIC_FOLDER]:
    folder.mkdir(exist_ok=True)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory=str(STATIC_FOLDER)), name="static")
    app.mount("/outputs", StaticFiles(directory=str(OUTPUT_FOLDER)), name="outputs")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")

# Store active sessions
sessions = {}
analyzers = {}
frame_queues = {}  # For frame streaming
processing_threads = {}

# Helper functions
def allowed_file(filename: str) -> bool:
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_frame_to_base64(frame):
    """Encode frame to base64 JPEG"""
    try:
        # Resize for faster transmission
        h, w = frame.shape[:2]
        if w > 1280:
            scale = 1280 / w
            frame = cv2.resize(frame, (int(w*scale), int(h*scale)))
        
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
        return base64.b64encode(buffer).decode('utf-8')
    except Exception as e:
        print(f"Frame encode error: {e}")
        return None

@app.get("/")
async def root():
    """API information"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Football Performance Analyzer API - Enhanced</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; }
            h1 { color: #2c3e50; }
            .feature { background: #e8f5e9; padding: 15px; margin: 10px 0; border-left: 4px solid #4caf50; }
            .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { display: inline-block; padding: 5px 10px; border-radius: 3px; font-weight: bold; }
            .get { background: #28a745; color: white; }
            .post { background: #007bff; color: white; }
            code { background: #e9ecef; padding: 2px 6px; border-radius: 3px; }
            .new { background: #ffc107; color: #000; padding: 2px 8px; border-radius: 3px; font-size: 0.8em; }
        </style>
    </head>
    <body>
        <h1>⚽ Football Performance Analyzer API v2.0 (Enhanced)</h1>
        <p>FastAPI server with streaming, WebSockets, and improved tracking</p>
        
        <h2>🚀 New Features:</h2>
        <div class="feature">
            <strong>📡 Frame Streaming:</strong> Real-time annotated frames via SSE
        </div>
        <div class="feature">
            <strong>🔌 WebSocket Support:</strong> Live progress updates
        </div>
        <div class="feature">
            <strong>🎯 Better Tracking:</strong> 8-second buffer, aggressive detection (conf=0.08)
        </div>
        <div class="feature">
            <strong>📊 Quality Monitoring:</strong> Track consistency throughout video
        </div>
        
        <h2>Available Endpoints:</h2>
        
        <div class="endpoint">
            <span class="method post">POST</span>
            <strong>/api/upload</strong>
            <p>Upload a video file for analysis</p>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span>
            <strong>/api/process</strong> <span class="new">ENHANCED</span>
            <p>Process uploaded video with streaming support</p>
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span>
            <strong>/api/stream/{session_id}</strong> <span class="new">NEW</span>
            <p>Stream annotated frames (Server-Sent Events)</p>
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span>
            <strong>/ws/progress/{session_id}</strong> <span class="new">NEW</span>
            <p>WebSocket for real-time progress updates</p>
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span>
            <strong>/api/player/{id}/stats</strong>
            <p>Get player statistics</p>
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span>
            <strong>/api/player/{id}/card</strong>
            <p>Get player performance card (PNG)</p>
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span>
            <strong>/api/player/{id}/heatmap</strong>
            <p>Get player movement heatmap (PNG)</p>
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span>
            <strong>/api/sessions</strong>
            <p>List active sessions</p>
        </div>
        
        <p style="margin-top: 30px; color: #6c757d;">
            Version 2.0.0 | Enhanced tracking | Frame streaming | WebSocket support
        </p>
    </body>
    </html>
    """)

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy",
        "service": "Football Performance Analyzer Enhanced",
        "version": "2.0.0",
        "features": ["streaming", "websocket", "aggressive_tracking"],
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(sessions),
        "processing": len(processing_threads)
    })

@app.post("/api/upload")
async def upload_video(video: UploadFile = File(...)):
    """Upload video file"""
    try:
        # Validate file
        if not allowed_file(video.filename):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Allowed: mp4, avi, mov, mkv"
            )
        
        # Create session
        session_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{session_id}_{timestamp}_{video.filename}"
        video_path = UPLOAD_FOLDER / filename
        
        # Save file
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        
        # Get video info
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = total_frames / fps if fps > 0 else 0
        cap.release()
        
        # Store session info
        sessions[session_id] = {
            "video_path": str(video_path),
            "filename": filename,
            "upload_time": datetime.now().isoformat(),
            "status": "uploaded"
        }
        
        return JSONResponse({
            "session_id": session_id,
            "video_path": str(video_path),
            "filename": filename,
            "video_info": {
                "fps": fps,
                "total_frames": total_frames,
                "width": width,
                "height": height,
                "duration_seconds": duration
            },
            "message": "Upload successful"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process")
async def process_video(
    background_tasks: BackgroundTasks,
    session_id: str = Form(...),
    video_path: str = Form(...),
    use_cache: bool = Form(True),
    enable_streaming: bool = Form(False)
):
    """Process video with optional frame streaming"""
    try:
        # Validate session
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Validate video exists
        if not Path(video_path).exists():
            raise HTTPException(status_code=404, detail="Video file not found")
        
        # Create or get analyzer
        if session_id not in analyzers:
            analyzers[session_id] = FootballPerformanceAnalyzer()
        
        # Create frame queue if streaming enabled
        if enable_streaming:
            frame_queues[session_id] = queue.Queue(maxsize=10)
        
        # Process in background
        def process_task():
            try:
                analyzer = analyzers[session_id]
                
                # Frame callback for streaming
                def frame_callback(frame):
                    if enable_streaming and session_id in frame_queues:
                        try:
                            # Non-blocking put with timeout
                            frame_queues[session_id].put(frame, block=False)
                        except queue.Full:
                            # Skip frame if queue full
                            pass
                
                print(f"\n🎬 Processing video for session {session_id}...")
                player_stats, player_images = analyzer.process_video(
                    video_path,
                    use_stubs=use_cache,
                    frame_callback=frame_callback if enable_streaming else None
                )
                
                # Signal end of stream
                if enable_streaming and session_id in frame_queues:
                    frame_queues[session_id].put(None)  # Sentinel
                
                # Update session
                sessions[session_id]["status"] = "processed"
                sessions[session_id]["player_count"] = len(player_stats)
                sessions[session_id]["process_time"] = datetime.now().isoformat()
                
                print(f"✅ Session {session_id} complete: {len(player_stats)} players")
                
            except Exception as e:
                print(f"❌ Processing error for {session_id}: {e}")
                import traceback
                traceback.print_exc()
                sessions[session_id]["status"] = "error"
                sessions[session_id]["error"] = str(e)
            finally:
                # Cleanup
                if session_id in processing_threads:
                    del processing_threads[session_id]
        
        # Start processing thread
        thread = threading.Thread(target=process_task, daemon=True)
        thread.start()
        processing_threads[session_id] = thread
        
        sessions[session_id]["status"] = "processing"
        
        return JSONResponse({
            "session_id": session_id,
            "status": "processing",
            "streaming_enabled": enable_streaming,
            "stream_url": f"/api/stream/{session_id}" if enable_streaming else None,
            "message": "Processing started"
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stream/{session_id}")
async def stream_frames(session_id: str):
    """Stream annotated frames via Server-Sent Events"""
    if session_id not in frame_queues:
        raise HTTPException(status_code=404, detail="No stream available for this session")
    
    async def generate():
        fq = frame_queues[session_id]
        frame_count = 0
        
        try:
            while True:
                try:
                    # Get frame from queue (blocking with timeout)
                    frame = fq.get(timeout=30)
                    
                    # Sentinel value means end of stream
                    if frame is None:
                        yield f"data: {json.dumps({'type': 'end'})}\n\n"
                        break
                    
                    # Encode to base64
                    frame_b64 = encode_frame_to_base64(frame)
                    if frame_b64:
                        frame_count += 1
                        data = {
                            'type': 'frame',
                            'frame_number': frame_count,
                            'data': frame_b64
                        }
                        yield f"data: {json.dumps(data)}\n\n"
                    
                    await asyncio.sleep(0.01)  # Small delay to prevent overwhelming
                    
                except queue.Empty:
                    # Send keepalive
                    yield f"data: {json.dumps({'type': 'keepalive'})}\n\n"
                    
        except Exception as e:
            print(f"Stream error: {e}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        finally:
            # Cleanup
            if session_id in frame_queues:
                del frame_queues[session_id]
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@app.get("/api/status/{session_id}")
async def get_status(session_id: str):
    """Get processing status"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    status = {
        "session_id": session_id,
        "status": session.get("status", "unknown"),
        "filename": session.get("filename"),
        "is_processing": session_id in processing_threads
    }
    
    if session.get("status") == "processed":
        if session_id in analyzers:
            status["player_count"] = len(analyzers[session_id].player_stats)
    
    if session.get("status") == "error":
        status["error"] = session.get("error")
    
    return JSONResponse(status)

@app.get("/api/session/{session_id}/players")
async def get_session_players(session_id: str):
    """Get all players for a session"""
    try:
        if session_id not in analyzers:
            raise HTTPException(status_code=404, detail="Session not found")
        
        analyzer = analyzers[session_id]
        
        players = []
        for player_id, stats in analyzer.player_stats.items():
            players.append({
                "player_id": int(player_id),
                "stats": stats,
                "has_image": player_id in analyzer.player_images
            })
        
        # Sort by total frames (most active first)
        players.sort(key=lambda x: x['stats']['total_frames'], reverse=True)
        
        return JSONResponse({
            "session_id": session_id,
            "total_players": len(players),
            "players": players
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/player/{player_id}/stats")
async def get_player_stats(player_id: int, session_id: str):
    """Get player statistics"""
    try:
        if session_id not in analyzers:
            raise HTTPException(status_code=404, detail="Session not found")
        
        analyzer = analyzers[session_id]
        
        if player_id not in analyzer.player_stats:
            raise HTTPException(status_code=404, detail="Player not found")
        
        return JSONResponse({
            "player_id": player_id,
            "stats": analyzer.player_stats[player_id],
            "has_image": player_id in analyzer.player_images
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/player/{player_id}/card")
async def get_player_card(player_id: int, session_id: str, format: str = "image"):
    """Get player card"""
    try:
        if session_id not in analyzers:
            raise HTTPException(status_code=404, detail="Session not found")
        
        analyzer = analyzers[session_id]
        
        if player_id not in analyzer.player_stats:
            raise HTTPException(status_code=404, detail="Player not found")
        
        if format == "json":
            return JSONResponse({
                "player_id": player_id,
                "stats": analyzer.player_stats[player_id]
            })
        
        # Generate card
        fig = analyzer.generate_player_card(player_id)
        if fig is None:
            raise HTTPException(status_code=500, detail="Cannot generate card")
        
        # Save to file
        output_path = OUTPUT_FOLDER / f"player_{player_id}_card_{session_id}.png"
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
        
        import matplotlib.pyplot as plt
        plt.close(fig)
        
        # Return file
        return FileResponse(
            output_path,
            media_type="image/png",
            filename=f"player_{player_id}_card.png"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/player/{player_id}/heatmap")
async def get_player_heatmap(player_id: int, session_id: str, bins: int = 60):
    """Get player heatmap"""
    try:
        if session_id not in analyzers:
            raise HTTPException(status_code=404, detail="Session not found")
        
        analyzer = analyzers[session_id]
        
        if player_id not in analyzer.player_stats:
            raise HTTPException(status_code=404, detail="Player not found")
        
        # Generate heatmap
        fig = analyzer.generate_heatmap(player_id, bins=bins)
        if fig is None:
            raise HTTPException(status_code=500, detail="Cannot generate heatmap")
        
        # Save to file
        output_path = OUTPUT_FOLDER / f"player_{player_id}_heatmap_{session_id}.png"
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
        
        import matplotlib.pyplot as plt
        plt.close(fig)
        
        # Return file
        return FileResponse(
            output_path,
            media_type="image/png",
            filename=f"player_{player_id}_heatmap.png"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/player/{player_id}/recovery")
async def get_recovery_plan(player_id: int, session_id: str):
    """Get recovery plan"""
    try:
        if session_id not in analyzers:
            raise HTTPException(status_code=404, detail="Session not found")
        
        analyzer = analyzers[session_id]
        
        if player_id not in analyzer.player_stats:
            raise HTTPException(status_code=404, detail="Player not found")
        
        # Generate recovery plan
        result = analyzer.generate_recovery_plan(player_id)
        if result is None:
            raise HTTPException(status_code=500, detail="Cannot generate recovery plan")
        
        return JSONResponse({
            "player_id": player_id,
            "injury_prediction": result["injury_prediction"],
            "recovery_plan": result["recovery_plan"],
            "text_report": result.get("text_report", ""),
            "recovery_card_path": result.get("recovery_card_path", "")
        })
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions")
async def list_sessions():
    """List active sessions"""
    session_list = []
    for sid, session in sessions.items():
        session_list.append({
            "session_id": sid,
            "filename": session.get("filename"),
            "status": session.get("status"),
            "upload_time": session.get("upload_time"),
            "is_processing": sid in processing_threads,
            "has_analyzer": sid in analyzers
        })
    
    return JSONResponse({
        "active_sessions": len(sessions),
        "processing": len(processing_threads),
        "sessions": session_list
    })

@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """Delete session and cleanup"""
    try:
        if session_id in sessions:
            # Delete video file
            video_path = sessions[session_id].get("video_path")
            if video_path and Path(video_path).exists():
                Path(video_path).unlink()
            
            # Remove from sessions
            del sessions[session_id]
            
            # Remove analyzer
            if session_id in analyzers:
                del analyzers[session_id]
            
            # Remove frame queue
            if session_id in frame_queues:
                del frame_queues[session_id]
            
            return JSONResponse({
                "message": "Session deleted",
                "session_id": session_id
            })
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export/{session_id}")
async def export_session(session_id: str):
    """Export session data to JSON"""
    try:
        if session_id not in analyzers:
            raise HTTPException(status_code=404, detail="Session not found")
        
        analyzer = analyzers[session_id]
        
        output_filename = f"analysis_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_path = OUTPUT_FOLDER / output_filename
        
        export_data = analyzer.export_to_json(str(output_path))
        
        return FileResponse(
            output_path,
            media_type="application/json",
            filename=output_filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("=" * 80)
    print("⚽ FOOTBALL ANALYZER - ENHANCED FASTAPI SERVER v2.0")
    print("=" * 80)
    print("\n✅ Features:")
    print("   📡 Real-time frame streaming (SSE)")
    print("   🎯 Aggressive tracking (8-second buffer, conf=0.08)")
    print("   📊 Quality monitoring throughout video")
    print("   🔧 Improved occlusion handling")
    print("\n=" * 80)
    print(f"\n📁 Folders:")
    print(f"   Upload: {UPLOAD_FOLDER}")
    print(f"   Output: {OUTPUT_FOLDER}")
    print(f"   Static: {STATIC_FOLDER}\n")
    print("=" * 80)
    print("\n🚀 Starting server...")
    print("📖 API docs: http://localhost:8000/docs")
    print("🏠 Home: http://localhost:8000")
    print("💡 Press Ctrl+C to stop\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")