import traceback
from viewmodels import ViewModel
from models.scripts_model import ScriptsModel
from data.scripts_data import ScriptsData

class ScriptsViewModel(ViewModel):
    def __init__(self, model=None, data=None, app=None):
        super().__init__(model or ScriptsModel(), data or ScriptsData())
        self.app = app
        self.scope = {
            "app": self.app,
            "vm_store": self.app.vm_store,
            "imgui": __import__("imgui_bundle").imgui,
            "print": self.capture_output
        }

    def capture_output(self, *args):
        self.data.output_log += " ".join(str(a) for a in args) + "\n"

    def refresh_script_list(self):
        self.data.script_list = self.model.list_scripts()

    def load_script(self, name):
        self.data.editor_content = self.model.load_script(name)
        self.data.code = self.data.editor_content

    def run_editor_script(self):
        try:
            self.data.output_log = ""
            self.model.run_code(self.data.editor_content, self.scope)
        except Exception:
            self.data.output_log = traceback.format_exc()

    def run_console_code(self):
        try:
            self.data.exec_result = ""
            self.model.run_code(self.data.code, self.scope)
        except Exception:
            self.data.exec_result = traceback.format_exc()