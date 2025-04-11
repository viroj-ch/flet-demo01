import flet as ft
from controls.date_picker import MyDatePicker
from controls.rule_control import RuleControl

class MyForm(ft.Column):
    def __init__(self):
        super().__init__()
        self.start_date = MyDatePicker('start_date', '20250301')
        self.end_date = MyDatePicker('end_date', '20250430')
        self.bzb_mission_id=ft.TextField(label="bzb_mission_id", value="MID0000001")
        self.submission_id=ft.TextField(label="submission_id", value="SMID000001")
        self.bzb_mission_id=ft.TextField(label="bzb_mission_id", value="MID0000001")
        self.submission_id=ft.TextField(label="submission_id", value="SMID000001")
        self.rule_control=RuleControl(submission_form=self)
        self.controls = [
            self.bzb_mission_id,
            self.submission_id,
            self.start_date,
            self.end_date,
            self.rule_control,
        ]

def main(page: ft.Page):
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width=500
    page.window.height=800
    page.padding=ft.Padding(top=20, right=10, bottom=20, left=10)
    page.window.top=50
    page.scroll=ft.ScrollMode.AUTO
    page.add(ft.AppBar(title=ft.Text("new submission (SQL generation)"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),)
    page.add(
        ft.Column(
            # expand=False,
            controls=[
                MyForm(),
            ],
            width= 500,
        ),
    )


if __name__ == "__main__":
    ft.app(main)
