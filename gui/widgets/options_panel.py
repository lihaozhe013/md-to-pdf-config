import json
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from converter import ensure_config, get_project_root
from i18n import _

PAGE_SIZES = ["A4", "A3", "A5", "Letter", "Legal"]
PDF_MARGINS = ["10mm", "15mm", "20mm", "25mm", "30mm"]


class OptionsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._css_files = self._find_css_files()
        self._default_css = self._read_config_css()
        self._setup_ui()

    def _find_css_files(self) -> list[Path]:
        root = get_project_root() / "css"
        return sorted(root.glob("*.css"))

    def _read_config_css(self) -> str | None:
        try:
            root = get_project_root()
            config_file = ensure_config(root)
            config = json.loads(config_file.read_text(encoding="utf-8"))
            stylesheets = config.get("stylesheet", [])
            return str(stylesheets[0]) if stylesheets else None
        except Exception:
            return None

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._group = QGroupBox()
        form = QFormLayout(self._group)
        form.setLabelAlignment(Qt.AlignRight)

        self._css_combo = QComboBox()
        for css in self._css_files:
            self._css_combo.addItem(css.name, str(css))
        self._select_css(self._default_css)
        self._css_label = QLabel()
        form.addRow(self._css_label, self._css_combo)

        dir_layout = QHBoxLayout()
        self._output_dir_edit = QLineEdit()
        self._output_dir_edit.setReadOnly(True)
        self._browse_btn = QPushButton()
        self._browse_btn.clicked.connect(self._on_browse)
        dir_layout.addWidget(self._output_dir_edit)
        dir_layout.addWidget(self._browse_btn)
        self._output_dir_label = QLabel()
        form.addRow(self._output_dir_label, dir_layout)

        self._filename_edit = QLineEdit()
        self._filename_label = QLabel()
        form.addRow(self._filename_label, self._filename_edit)

        self._page_size_combo = QComboBox()
        self._page_size_combo.addItems(PAGE_SIZES)
        self._page_size_combo.setCurrentText("A4")
        self._page_size_label = QLabel()
        form.addRow(self._page_size_label, self._page_size_combo)

        self._margin_combo = QComboBox()
        self._margin_combo.addItems(PDF_MARGINS)
        self._margin_combo.setCurrentText("20mm")
        self._margin_label = QLabel()
        form.addRow(self._margin_label, self._margin_combo)

        self._footer_check = QCheckBox()
        self._footer_check.setChecked(True)
        form.addRow("", self._footer_check)

        layout.addWidget(self._group)

        self.retranslate_ui()

    def retranslate_ui(self):
        self._group.setTitle(_("Options"))
        self._css_label.setText(_("CSS Theme:"))
        self._output_dir_label.setText(_("Output Directory:"))
        self._output_dir_edit.setPlaceholderText(_("Not selected, output to same directory as source"))
        self._browse_btn.setText(_("Browse…"))
        self._filename_label.setText(_("Output Filename:"))
        self._filename_edit.setPlaceholderText(_("Default to source filename"))
        self._page_size_label.setText(_("Page Size:"))
        self._margin_label.setText(_("Margin:"))
        self._footer_check.setText(_("Show Footer Page Numbers"))

    def _on_browse(self):
        directory = QFileDialog.getExistingDirectory(self, _("Select Output Directory"))
        if directory:
            self._output_dir_edit.setText(directory)

    def _select_css(self, css_path: str | None) -> None:
        if not css_path:
            return
        for i in range(self._css_combo.count()):
            if self._css_combo.itemData(i) == css_path:
                self._css_combo.setCurrentIndex(i)
                return

    def set_output_filename(self, name: str) -> None:
        if not self._filename_edit.text():
            self._filename_edit.setText(name)

    @property
    def css_path(self) -> str | None:
        return self._css_combo.currentData()

    @property
    def output_dir(self) -> str | None:
        text = self._output_dir_edit.text().strip()
        return text if text else None

    @property
    def output_filename(self) -> str:
        return self._filename_edit.text().strip()

    @property
    def page_size(self) -> str:
        return self._page_size_combo.currentText()

    @property
    def margin(self) -> str:
        return self._margin_combo.currentText()

    @property
    def show_footer(self) -> bool:
        return self._footer_check.isChecked()
