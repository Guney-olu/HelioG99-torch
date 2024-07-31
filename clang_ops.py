import ctypes
import subprocess
import pathlib
import tempfile
from tinygrad.device import Compiled, Compiler, MallocAllocator
from tinygrad.helpers import cpu_time_execution, DEBUG, cpu_objdump
from tinygrad.renderer.cstyle import ClangRenderer

class ClangCompiler(Compiler):
    def compile(self, src: str) -> bytes:
    
        with tempfile.NamedTemporaryFile(delete=False, suffix=".so") as output_file:
            output_file_path = output_file.name


        try:
            subprocess.check_output([
                'clang', '-include', 'tgmath.h', '-shared', '-march=native', '-O2', '-Wall', '-Werror', '-x', 'c', '-fPIC',
                '-lm', '-L/system/lib64', '-L/data/data/com.termux/files/usr/lib', '-o', output_file_path, '-'
            ], input=src.encode('utf-8'))
            return pathlib.Path(output_file_path).read_bytes()
        finally:
            pathlib.Path(output_file_path).unlink()

class ClangProgram:
    def __init__(self, name: str, lib: bytes):
        if DEBUG >= 6:
            cpu_objdump(lib)
        self.name, self.lib = name, lib

        # Write to disk so we can load it
        with tempfile.NamedTemporaryFile(delete=False, suffix=".so") as cached_file_path:
            cached_file_path.write(lib)
            self.fxn = ctypes.CDLL(cached_file_path.name)[name]

    def __call__(self, *bufs, vals=(), wait=False):
        return cpu_time_execution(lambda: self.fxn(*bufs, *vals), enable=wait)

class ClangDevice(Compiled):
    def __init__(self, device: str):
        from tinygrad.runtime.graph.clang import ClangGraph
        super().__init__(device, MallocAllocator, ClangRenderer(), ClangCompiler("compile_clang"), ClangProgram, ClangGraph)

