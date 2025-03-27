import flet as ft
from controls.date_picker import MyDatePicker
from controls.rule_control import RuleControl
from services.gen_submission_sql import SubmissionSQL

class MyForm(ft.Column):
    def __init__(self):
        super().__init__()
        self.start_date = MyDatePicker('start_date', '20250301')
        self.end_date = MyDatePicker('end_date', '20250430')
        self.bzb_mission_id=ft.TextField(label="bzb_mission_id", value="MID0000001")
        self.submission_id=ft.TextField(label="submission_id", value="SMID000001")
        self.bzb_mission_id=ft.TextField(label="bzb_mission_id", value="MID0000001")
        self.submission_id=ft.TextField(label="submission_id", value="SMID000001")
        self.rule_control=RuleControl()
        self.controls = [
            self.bzb_mission_id,
            self.submission_id,
            self.start_date,
            self.end_date,
            self.rule_control,
            ft.ElevatedButton("get SQL", on_click=self.gen_sql_handle_click),
        ]

    def gen_sql_handle_click(self, e: ft.ControlEvent):
        data = {
            "submission_id": self.submission_id.value,
            "rule_id": self.rule_control.rule_id.value,
            "bzb_mission_id": self.bzb_mission_id.value,
            "sql_argument_value": {
                "start_date": self.start_date.value,
                "end_date": self.end_date.value,
            }
        }
        if self.rule_control.sub_account.visible: data['sql_argument_value']['sub_account'] = self.rule_control.sub_account.value
        if self.rule_control.amount.visible: data['sql_argument_value']['amount'] = self.rule_control.amount.value
        if self.rule_control.number_of_days.visible: data['sql_argument_value']['number_of_days'] = self.rule_control.number_of_days.value
        if self.rule_control.times.visible: data['sql_argument_value']['times'] = self.rule_control.times.value

        sqlObject = SubmissionSQL(data)
        self.page.open(ft.SnackBar(ft.Text(sqlObject.get_value(), size=15)))
        print(sqlObject.get_value())
        self.page.set_clipboard(sqlObject.get_value())

def main(page: ft.Page):
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width=500
    page.window.height=800
    page.padding=ft.Padding(top=20, right=10, bottom=20, left=10)
    # page.window.top=50
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
