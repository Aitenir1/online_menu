from fpdf import FPDF

from MotionWeb.settings import FONT_PATH


class Cheque(FPDF):
    def __init__(self, date, table, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = date
        self.table = table

    def header(self):
        print(f"{FONT_PATH=}")
        self.add_font('DejaVu', '', FONT_PATH, uni=True)
        self.set_font("DejaVu", '', 8)

        self.cell(0, 5, "Кофейня \"Мой мир\"", 0, 1, "C")
        self.cell(0, 2, f"Дата: {self.date}", 0, 1, "C")
        self.cell(0, 5, f"Стол: {self.table}", 0, 1, "C")

        self.ln(3)
