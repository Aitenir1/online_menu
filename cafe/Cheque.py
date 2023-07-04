from fpdf import FPDF

from MotionWeb.settings.base import FONT_PATH

BORDERS = 0

class Cheque(FPDF):
    def __init__(self, date, table, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = date
        self.table = table

    def header(self):
        print(f"{FONT_PATH=}")

        self.add_font('DejaVu', '', FONT_PATH, uni=True)
        self.set_font("DejaVu", '', 7)
        self.set_margins(1, 0.5, 1)
        self.set_top_margin(1.5)

        self.cell(0, 0, "", 0, 1, "C")
        self.cell(0, 3, "Кофейня \"Мой мир\"", BORDERS, 1, "C")
        self.cell(0, 2.5, f"Дата: {self.date}", BORDERS, 1, "C")
        self.cell(0, 2.5, f"Стол: {self.table}", BORDERS, 1, "C")

        self.ln(3)


