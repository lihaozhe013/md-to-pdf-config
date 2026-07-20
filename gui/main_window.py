from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from converter import check_md_to_pdf
from i18n import _, current_lang, load_language

from .converter_thread import ConverterThread
from .widgets.drop_area import DropArea
from .widgets.options_panel import OptionsPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._thread: ConverterThread | None = None
        self._current_file_name: str | None = None
        self._status_success: bool | None = None
        self._status_output: str | None = None
        self._status_error: str | None = None
        self._dependency_warning_shown = False
        self._setup_ui()
        self._apply_style()
        self._check_dependencies()

    def _setup_ui(self):
        self.setMinimumSize(600, 550)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        top_bar = QHBoxLayout()
        top_bar.addStretch()
        lang_label = QLabel()
        self._lang_label = lang_label
        top_bar.addWidget(lang_label)
        self._lang_combo = QComboBox()
        self._lang_combo.addItem("中文", "zh_CN")
        self._lang_combo.addItem("English", "en")
        idx = self._lang_combo.findData(current_lang())
        if idx >= 0:
            self._lang_combo.setCurrentIndex(idx)
        self._lang_combo.currentIndexChanged.connect(self._on_language_changed)
        top_bar.addWidget(self._lang_combo)
        layout.addLayout(top_bar)

        self._drop_area = DropArea()
        self._drop_area.file_selected.connect(self._on_file_selected)
        layout.addWidget(self._drop_area)

        self._options_panel = OptionsPanel()
        layout.addWidget(self._options_panel)

        self._convert_btn = QPushButton()
        self._convert_btn.setMinimumHeight(40)
        self._convert_btn.setCursor(Qt.PointingHandCursor)
        self._convert_btn.clicked.connect(self._on_convert)
        self._convert_btn.setEnabled(False)
        layout.addWidget(self._convert_btn)

        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 0)
        self._progress_bar.setVisible(False)
        self._progress_bar.setFixedHeight(6)
        layout.addWidget(self._progress_bar)

        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setMaximumHeight(120)
        layout.addWidget(self._log)

        self._status_label = QLabel()
        self._status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._status_label)

        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(_("md-to-pdf GUI"))
        self._lang_label.setText(_("Language") + ":")
        self._convert_btn.setText(_("Start Conversion") if not self._thread else _("Converting..."))
        self._log.setPlaceholderText(_("Log..."))
        if self._status_success is True:
            self._status_label.setText(_("✓ Conversion successful"))
        elif self._status_success is False:
            self._status_label.setText(_("✗ Conversion failed"))
        else:
            self._status_label.setText(_("Ready"))

    def _apply_style(self):
        p = self.palette()
        accent = p.color(QPalette.Highlight).name()
        accent_text = p.color(QPalette.HighlightedText).name()
        base = p.color(QPalette.Base).name()
        text_color = p.color(QPalette.Text).name()
        window = p.color(QPalette.Window).name()

        self._convert_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {accent};
                color: {accent_text};
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {QColor(accent).darker(110).name()};
            }}
            QPushButton:disabled {{
                background-color: {QColor(accent).lighter(140).name()};
                color: {QColor(accent_text).lighter(150).name()};
            }}
        """)

        self._log.setStyleSheet(f"""
            QTextEdit {{
                background-color: {base};
                color: {text_color};
                border: 1px solid {p.color(QPalette.Mid).name()};
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }}
        """)

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {window};
            }}
        """)

    def _check_dependencies(self):
        if not check_md_to_pdf():
            self._dependency_warning_shown = True
            self._log.append(_("⚠ md-to-pdf not installed! Run: npm i -g md-to-pdf"))

    def _on_language_changed(self, index: int):
        lang = self._lang_combo.itemData(index)
        load_language(lang)
        self.retranslate_ui()
        self._drop_area.retranslate_ui()
        self._options_panel.retranslate_ui()
        if self._dependency_warning_shown:
            self._log.clear()
            self._log.append(_("⚠ md-to-pdf not installed! Run: npm i -g md-to-pdf"))

    def _on_file_selected(self, path: str):
        self._convert_btn.setEnabled(True)
        self._current_file_name = Path(path).name
        stem = Path(path).stem
        self._options_panel.set_output_filename(stem + ".pdf")
        self._status_output = path
        self._log.append(_("Selected: {path}").format(path=path))

    def _on_convert(self):
        md_path = self._drop_area.file_path
        if not md_path:
            return

        css_path = self._options_panel.css_path
        if not css_path:
            self._log.append(_("Error: CSS file not found"))
            return

        md_file = Path(md_path)
        output_dir = self._options_panel.output_dir
        filename = self._options_panel.output_filename or f"{md_file.stem}.pdf"
        output_path = str(Path(output_dir) / filename) if output_dir else str(md_file.with_suffix(".pdf"))

        self._set_ui_busy(True)
        self._log.append(_("Converting: {name}").format(name=md_file.name))

        self._thread = ConverterThread(
            md_path=md_path,
            css_path=css_path,
            output_path=output_path,
            page_size=self._options_panel.page_size,
            margin=self._options_panel.margin,
            show_footer=self._options_panel.show_footer,
        )
        self._thread.started.connect(lambda name: self._log.append(_("Processing: {name}").format(name=name)))
        self._thread.progress.connect(lambda msg: self._log.append(msg))
        self._thread.finished.connect(self._on_conversion_done)
        self._thread.start()

    def _on_conversion_done(self, result):
        self._set_ui_busy(False)
        if result.success:
            self._status_success = True
            self._status_label.setText(_("✓ Conversion successful"))
            self._log.append(_("✓ Success: {output_path}").format(output_path=result.output_path))
        else:
            self._status_success = False
            self._status_label.setText(_("✗ Conversion failed"))
            self._log.append(_("✗ Failed: {error}").format(error=result.error))
        self._thread = None

    def _set_ui_busy(self, busy: bool):
        self._convert_btn.setEnabled(not busy)
        self._convert_btn.setText(_("Converting...") if busy else _("Start Conversion"))
        self._progress_bar.setVisible(busy)
        self._drop_area.setAcceptDrops(not busy)
