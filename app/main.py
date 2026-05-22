from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import os
import shutil
import time
from app.services.ingestion import IngestionService
from app.services.vector_store import VectorStoreService
from app.services.rag_service import RAGService
from app.utils.config import DATA_DIR, VECTORSTORE_DIR
from pydantic import BaseModel
from nicegui import ui, app as nicegui_app, run

# --- Backend Services ---
ingestion_service = IngestionService()
vector_store_service = VectorStoreService()
rag_service = RAGService(vector_store_service=vector_store_service)

# --- FastAPI Setup ---
app = FastAPI(title="IntraBot API")

class QueryRequest(BaseModel):
    query: str
    document_name: str = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@app.post("/upload")
async def upload_document(files: List[UploadFile] = File(...)):
    saved_paths = []
    for file in files:
        file_path = os.path.join(DATA_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_paths.append(file_path)
    
    try:
        chunks = ingestion_service.process_documents(saved_paths)
        if chunks:
            vector_store_service.create_or_update_index(chunks)
            return {"message": f"Successfully indexed {len(files)} documents."}
        return {"message": "No valid text chunks found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_bot(request: QueryRequest):
    try:
        result = rag_service.query(request.query, doc_name=request.document_name)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query error: {str(e)}")

# --- NiceGUI UI Implementation ---

# Custom Styles for Claymorphism and Effects
UI_STYLES = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    body {
        font-family: 'Outfit', sans-serif;
        background: #020617; /* Deep base */
        margin: 0;
    }

    /* Aurora Glow Animation */
    .aurora {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(135deg, #020617 0%, #1e1b4b 25%, #1e293b 50%, #1e1b4b 75%, #020617 100%);
        background-size: 400% 400%;
        animation: auroraFlow 20s ease infinite;
        z-index: -2;
        opacity: 0.8;
    }

    @keyframes auroraFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Floating Main Card */
    .floating-card {
        animation: floating 6s ease-in-out infinite;
    }

    @keyframes floating {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    /* Claymorphism Cards 2.0 */
    .clay-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 28px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 15px 15px 35px rgba(0, 0, 0, 0.4),
                    inset -8px -8px 20px rgba(255, 255, 255, 0.05),
                    inset 8px 8px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .clay-card:hover {
        border-color: rgba(59, 130, 246, 0.4);
        box-shadow: 20px 20px 45px rgba(0, 0, 0, 0.5),
                    inset -8px -8px 20px rgba(255, 255, 255, 0.08);
    }

    /* Shimmering Chat Bubbles */
    .chat-bubble-user {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 24px 24px 4px 24px;
        padding: 14px 20px;
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
        align-self: flex-end;
    }

    .chat-bubble-bot {
        background: rgba(15, 23, 42, 0.8);
        color: #f1f5f9;
        border-radius: 24px 24px 24px 4px;
        padding: 14px 20px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.08);
        align-self: flex-start;
        position: relative;
        overflow: hidden;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.95) translateY(10px); }
        to { opacity: 1; transform: scale(1) translateY(0); }
    }

    .animate-fade {
        animation: fadeIn 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    }

    /* Interactive Particles Layer */
    #particles-js {
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        z-index: -1;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(59, 130, 246, 0.3); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(59, 130, 246, 0.5); }
</style>
<div class="aurora"></div>
<div id="particles-js"></div>
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script>
    particlesJS('particles-js', {
        particles: {
            number: { value: 80, density: { enable: true, value_area: 1000 } },
            color: { value: ['#3b82f6', '#8b5cf6', '#60a5fa'] },
            shape: { type: 'circle' },
            opacity: { value: 0.4, random: true, anim: { enable: true, speed: 1, opacity_min: 0.1 } },
            size: { value: 3, random: true, anim: { enable: true, speed: 2, size_min: 0.1 } },
            line_linked: { enable: true, distance: 150, color: '#3b82f6', opacity: 0.2, width: 1 },
            move: { enable: true, speed: 2, direction: 'none', random: true, straight: false, out_mode: 'out' }
        },
        interactivity: {
            detect_on: 'window',
            events: { onhover: { enable: true, mode: 'bubble' }, onclick: { enable: true, mode: 'push' } },
            modes: { 
                bubble: { distance: 200, size: 6, duration: 0.3, opacity: 0.8 },
                push: { particles_nb: 4 }
            }
        }
    });
</script>
"""

@ui.page('/')
async def main_page():
    ui.add_head_html(UI_STYLES)
    
    # State management
    chat_container = None
    selected_doc = "All Documents"
    
    def select_document(doc_name):
        nonlocal selected_doc
        selected_doc = doc_name
        doc_list.refresh()
        ui.notify(f'Selected: {doc_name}', type='info', position='bottom-right')

    async def delete_document(doc_name):
        nonlocal selected_doc
        path = os.path.join(DATA_DIR, doc_name)
        try:
            if os.path.exists(path):
                os.remove(path)
                ui.notify(f'Deleted {doc_name} from disk.', type='info')
            
            # Reset selection if deleted
            if selected_doc == doc_name:
                selected_doc = "All Documents"
            
            # Refresh Knowledge Base (Full Sync)
            ui.notify('Updating knowledge base...', type='info')
            await auto_sync()
            doc_list.refresh()
            ui.notify(f'Successfully removed {doc_name}', type='positive')
        except Exception as ex:
            ui.notify(f'Delete failed: {str(ex)}', type='negative')
            print(f"\033[91m[DELETE]\033[0m Error: {str(ex)}")
    
    async def send_message():
        msg = input_field.value
        if not msg: return
        
        input_field.value = ''
        with chat_container:
            ui.markdown(f'**You:** {msg}').classes('chat-bubble-user animate-fade')
            bot_msg_wrapper = ui.column().classes('chat-bubble-bot animate-fade w-full')
            with bot_msg_wrapper:
                loading = ui.spinner(size='md', color='blue')
                
        # Call RAG Service
        try:
            start_time = time.perf_counter()
            result = await run.io_bound(rag_service.query, msg, doc_name=selected_doc)
            duration = time.perf_counter() - start_time
            print(f"\033[94m[OLLAMA]\033[0m Response generated in \033[92m{duration:.2f}s\033[0m")
            
            loading.delete()
            with bot_msg_wrapper:
                ui.markdown(result['answer'])
                if result.get('sources'):
                    with ui.row().classes('mt-2 flex-wrap gap-1'):
                        for src in set(result['sources']):
                            ui.label(os.path.basename(src)).classes('text-xs bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded-full border border-blue-500/30')
        except Exception as e:
            loading.delete()
            with bot_msg_wrapper:
                ui.label(f'Error: {str(e)}').classes('text-red-400')
        
        await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')

    import inspect
    async def handle_upload(e):
        try:
            name = getattr(e, 'name', None)
            file_obj = getattr(e, 'file', None)
            
            if file_obj:
                name = file_obj.name
                path = os.path.join(DATA_DIR, name)
                print(f"\n\033[94m[UPLOAD]\033[0m Processing file via e.file: {name}")
                
                content = file_obj.read()
                if inspect.iscoroutine(content):
                    content = await content
                    
                with open(path, 'wb') as f:
                    f.write(content if isinstance(content, bytes) else content.encode('utf-8'))
            elif hasattr(e, 'content') and name:
                path = os.path.join(DATA_DIR, name)
                print(f"\n\033[94m[UPLOAD]\033[0m Processing file via e.content: {name}")
                with open(path, 'wb') as f:
                    f.write(e.content.read())
            else:
                print(f"\033[91m[ERROR]\033[0m Could not extract file information from event. Attributes: {dir(e)}")
                return
                
            ui.notify(f'Uploaded {name}. Indexing...', type='info')
            
            # Process this specific file
            chunks = await run.io_bound(ingestion_service.process_documents, [path])
            if chunks:
                await run.io_bound(vector_store_service.create_or_update_index, chunks)
                ui.notify(f'Indexed {name}!', type='positive')
                print(f"\033[92m[UPLOAD]\033[0m Successfully indexed {name} and refreshed sidebar.")
                doc_list.refresh()
            else:
                ui.notify(f'No usable text in {name}.', type='warning')
                print(f"\033[93m[UPLOAD]\033[0m No chunks extracted from {name}.")
        except Exception as ex:
            ui.notify(f'Indexing failed: {str(ex)}', type='negative')
            print(f"\033[91m[UPLOAD]\033[0m Error during processing: {str(ex)}")

    @ui.refreshable
    def doc_list():
        files = sorted(os.listdir(DATA_DIR)) if os.path.exists(DATA_DIR) else []
        with ui.column().classes('w-full gap-2 p-4'):
            ui.label('Knowledge Base').classes('text-lg font-bold text-blue-400 mb-2')
            
            # "All Documents" option
            is_all = selected_doc == "All Documents"
            with ui.row().on('click', lambda: select_document("All Documents")).classes(
                f'w-full items-center justify-between p-3 rounded-xl border transition-all cursor-pointer '
                f'{"bg-blue-500/20 border-blue-500/50" if is_all else "bg-slate-800/30 border-slate-700/50 hover:bg-slate-800/60"}'
            ):
                with ui.row().classes('items-center gap-3'):
                    ui.icon('apps', color='blue-400' if is_all else 'slate-400')
                    ui.label('All Documents').classes(f'text-sm {"text-blue-200 font-bold" if is_all else "text-slate-400"}')
                if is_all:
                    ui.icon('check_circle', color='blue-400').classes('text-sm')

            ui.separator().classes('bg-slate-800 my-2')

            if not files:
                ui.label('No documents uploaded.').classes('text-slate-500 italic px-2')
            for f in files:
                is_selected = selected_doc == f
                with ui.row().classes('w-full items-center gap-1'):
                    # Document Selectable Area
                    with ui.row().on('click', lambda f=f: select_document(f)).classes(
                        f'flex-grow items-center justify-between p-3 rounded-xl border transition-all cursor-pointer '
                        f'{"bg-blue-600/30 border-blue-500/60 shadow-[0_0_15px_rgba(59,130,246,0.2)]" if is_selected else "bg-slate-800/50 border-slate-700 hover:border-slate-600"}'
                    ):
                        with ui.row().classes('items-center gap-2 overflow-hidden'):
                            ui.icon('description', color='blue-400' if is_selected else 'slate-500')
                            ui.label(f).classes(f'text-sm truncate w-32 {"text-white font-medium" if is_selected else "text-slate-300"}')
                        if is_selected:
                            ui.icon('check_circle', color='blue-400').classes('text-sm shadow-glow')
                        else:
                            ui.icon('radio_button_unchecked', color='slate-600').classes('text-sm')
                    
                    # Delete Button
                    ui.button(icon='delete', on_click=lambda f=f: delete_document(f)).props('flat round color=red-400 size=sm').classes('hover:bg-red-500/20')

    # Main Layout
    with ui.header(elevated=False).classes('bg-slate-900/80 backdrop-blur-md border-b border-slate-700 py-4'):
        with ui.row().classes('w-full items-center justify-between px-6'):
            with ui.row().classes('items-center gap-3'):
                ui.icon('bolt', color='blue-500').classes('text-3xl')
                ui.label('IntraBot').classes('text-2xl font-bold tracking-tight text-white')
            ui.button(icon='refresh', on_click=lambda: doc_list.refresh()).props('flat round color=white')

    with ui.left_drawer(value=True).classes('bg-slate-900/50 backdrop-blur-xl border-r border-slate-800 p-0').props('width=300'):
        with ui.column().classes('h-full w-full'):
            doc_list()
            ui.space()
            with ui.column().classes('w-full p-4 border-t border-slate-800 bg-slate-900/80'):
                ui.upload(on_upload=handle_upload, multiple=True, label='Upload policies').classes('w-full').props('auto-upload dark')

    with ui.column().classes('w-full max-w-4xl mx-auto h-[calc(100vh-80px)] p-6 gap-6 floating-card'):
        # Chat History
        with ui.scroll_area().classes('flex-grow w-full clay-card p-6') as scroller:
            chat_container = ui.column().classes('w-full gap-4')
        
        # Input Area
        with ui.row().classes('w-full gap-4 items-center clay-card p-4 mb-4'):
            input_field = ui.input(placeholder='Ask about HR policies...').classes('flex-grow text-white').props('borderless dark').on('keydown.enter', send_message)
            ui.button(icon='send', on_click=send_message).props('round color=blue size=lg shadow-lg').classes('hover:scale-110 transition-transform')

# --- Startup Logic: Auto-Sync Index ---
async def auto_sync():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    files = [f for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]
    if not files:
        print(f"\033[93m[SYSTEM]\033[0m No files found in {DATA_DIR}")
        return
        
    print(f"\033[94m[SYSTEM]\033[0m Found {len(files)} files: {files}")
    print(f"\033[94m[SYSTEM]\033[0m Refreshing knowledge base...")
    try:
        paths = [os.path.join(DATA_DIR, f) for f in files]
        chunks = await run.io_bound(ingestion_service.process_documents, paths)
        if chunks:
            await run.io_bound(vector_store_service.recreate_index, chunks)
            print(f"\033[92m[SUCCESS]\033[0m Knowledge base refreshed and ready.")
        else:
            print(f"\033[93m[WARNING]\033[0m No usable text found in data files.")
    except Exception as e:
        print(f"\033[91m[ERROR]\033[0m Auto-sync failed: {str(e)}")

nicegui_app.on_startup(auto_sync)

# Initialize NiceGUI
ui.run_with(app, title="IntraBot - Local HR Assistant")

if __name__ == "__main__":
    import uvicorn
    # NiceGUI handles its own startup when run directly, but we use uvicorn for FastAPI integration
    # Since we used ui.run_with(app), we run the FastAPI app 'app'
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
