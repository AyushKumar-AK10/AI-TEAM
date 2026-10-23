from langchain_core.tools import tool
from ..Output.output import ResponseOutput
from pathlib import Path
import shutil

@tool
def fc(devOutput: list[ResponseOutput]) -> None:
    '''Function for creating the required files'''
    output_dir = Path('./Output')
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_root = output_dir.resolve()
    for file in devOutput:
        path = Path(file.path)
        code = file.code
        file_path = (output_root/path).resolve()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(code, encoding="utf-8")



    
