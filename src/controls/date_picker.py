import flet as ft

class MyDatePicker(ft.TextField):
    def __init__(self, label, value):
        super().__init__()
        # self.is_isolated= True
        self.label=label
        self.value=value
        self.suffix = ft.IconButton(
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: self.page.open(
                ft.DatePicker( on_change=self.handle_change, )
            ),
        )

    def handle_change(self,e):
        self.value = e.control.value.strftime('%Y%m%d')
        self.update()