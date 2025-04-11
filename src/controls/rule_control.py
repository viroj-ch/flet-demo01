import flet as ft
from services.gen_submission_sql import SubmissionSQL


class RuleId(ft.Dropdown):
    def __init__(self, rule_control):
        super().__init__()
        self.label="rule_id"
        self.rule_control=rule_control
        self.options = self.get_rule_options()
        self.on_change=self.rule_dropdown_changed
        self.value='R0001'

    def did_mount(self):        
        self.rule_dropdown_changed(ft.ControlEvent(
            target=self,
            name="1st change",
            data=self.value,
            control=self,
            page=self.page
            )
        )

    def get_rule_options(self):
        options = []
        options.append( ft.DropdownOption( key='R0001', content=ft.Text(value='R0001'), ) )
        options.append( ft.DropdownOption( key='R0002', content=ft.Text(value='R0002'), ) )
        options.append( ft.DropdownOption( key='R0003', content=ft.Text(value='R0003'), ) )
        options.append( ft.DropdownOption( key='R0004', content=ft.Text(value='R0004'), ) )
        options.append( ft.DropdownOption( key='R0005', content=ft.Text(value='R0005'), ) )
        options.append( ft.DropdownOption( key='R0006', content=ft.Text(value='R0006'), ) )
        options.append( ft.DropdownOption( key='R0007', content=ft.Text(value='R0007'), ) )
        options.append( ft.DropdownOption( key='R0008', content=ft.Text(value='R0008'), ) )
        options.append( ft.DropdownOption( key='R0009', content=ft.Text(value='R0009'), ) )
        return options        

    def rule_dropdown_changed(self, e: ft.ControlEvent):
        match e.control.value:
            case 'R0001':
                self.rule_control.sub_account.visible = False
                self.rule_control.amount.visible = False
                self.rule_control.number_of_days.visible = False
                self.rule_control.times.visible = False
            case 'R0002'|'R0003':
                self.rule_control.sub_account.visible = True
                self.rule_control.amount.visible = False
                self.rule_control.number_of_days.visible = True
                self.rule_control.times.visible = False
            case 'R0004':
                self.rule_control.sub_account.visible = True
                self.rule_control.amount.visible = True
                self.rule_control.number_of_days.visible = False
                self.rule_control.times.visible = False
            case 'R0005':
                self.rule_control.sub_account.visible = True
                self.rule_control.amount.visible = True
                self.rule_control.number_of_days.visible = True
                self.rule_control.times.visible = False
            case 'R0006':
                self.rule_control.sub_account.visible = True
                self.rule_control.amount.visible = True
                self.rule_control.number_of_days.visible = True
                self.rule_control.times.visible = True
            case 'R0007':
                self.rule_control.sub_account.visible = True
                self.rule_control.amount.visible = True
                self.rule_control.number_of_days.visible = False
                self.rule_control.times.visible = True
            case 'R0008':
                self.rule_control.sub_account.visible = False
                self.rule_control.amount.visible = True
                self.rule_control.number_of_days.visible = False
                self.rule_control.times.visible = False
            case 'R0009':
                self.rule_control.sub_account.visible = False
                self.rule_control.amount.visible = True
                self.rule_control.number_of_days.visible = False
                self.rule_control.times.visible = True
        self.rule_control.sql_result.value=''
        self.rule_control.update()


class SubAccount(ft.Dropdown):
    def __init__(self):
        super().__init__()
        self.label="sub_account"
        self.options = self.get_sub_account_options()
        self.value ='SA01'
        self.width=200

    def get_sub_account_options(self):
        options = []
        options.append( ft.DropdownOption( key='SA01', content=ft.Text(value='SA01'), ) )
        options.append( ft.DropdownOption( key='SA02', content=ft.Text(value='SA02'), ) )
        options.append( ft.DropdownOption( key='SA03', content=ft.Text(value='SA03'), ) )
        options.append( ft.DropdownOption( key='SA04', content=ft.Text(value='SA04'), ) )
        options.append( ft.DropdownOption( key='SA05', content=ft.Text(value='SA05'), ) )
        return options


class RuleControl(ft.Column):
    def __init__(self, submission_form):
        super().__init__()
        
        self.submission_form=submission_form
        self.rule_id=RuleId(rule_control=self)
        self.sub_account=SubAccount()
        self.amount=ft.TextField(label="amount", value=100, input_filter=ft.InputFilter(regex_string=r"^(\d+(\.\d*)?|\.\d+)$", allow=True))
        self.number_of_days=ft.TextField(label="number_of_days", value=10, input_filter=ft.NumbersOnlyInputFilter())
        self.times=ft.TextField(label="times",value=1,input_filter=ft.NumbersOnlyInputFilter(),keyboard_type=ft.KeyboardType.NUMBER,)
        self.sql_gen_button=GenSQLControl(submission_form=self.submission_form)
        self.sql_statment=''
        self.sql_result=ft.Markdown(value='', selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB, code_theme=ft.MarkdownCodeTheme.ATOM_ONE_LIGHT, )

        self.controls = [
            self.rule_id,
            self.sub_account,
            self.amount,
            self.number_of_days,
            self.times,
            self.sql_gen_button,
            self.sql_result,
        ]
    # def did_mount(self):
    #     self.controls.append(self.rule_id)
    #     self.controls.append(self.sub_account)
    #     self.controls.append(self.amount)
    #     self.controls.append(self.number_of_days)
    #     self.controls.append(self.times)
    #     self.controls.append(self.sql_gen_button)
    #     self.controls.append(self.sql_result)
    #     self.update()
        
class GenSQLControl(ft.ElevatedButton):
    def __init__(self, submission_form):
        super().__init__()
        self.submission_form=submission_form
        self.text="get SQL"
        self.on_click=self.gen_sql_handle_click

    def gen_sql_handle_click(self, e: ft.ControlEvent):
        data = {
            "submission_id": self.submission_form.submission_id.value,
            "rule_id": self.submission_form.rule_control.rule_id.value,
            "bzb_mission_id": self.submission_form.bzb_mission_id.value,
            "sql_argument_value": {
                "start_date": self.submission_form.start_date.value,
                "end_date": self.submission_form.end_date.value,
            }
        }
        if self.submission_form.rule_control.sub_account.visible: data['sql_argument_value']['sub_account'] = self.submission_form.rule_control.sub_account.value
        if self.submission_form.rule_control.amount.visible: data['sql_argument_value']['amount'] = self.submission_form.rule_control.amount.value
        if self.submission_form.rule_control.number_of_days.visible: data['sql_argument_value']['number_of_days'] = self.submission_form.rule_control.number_of_days.value
        if self.submission_form.rule_control.times.visible: data['sql_argument_value']['times'] = self.submission_form.rule_control.times.value

        sqlObject = SubmissionSQL(data)
        self.sql_statment = sqlObject.get_value()
        self.submission_form.page.open(ft.SnackBar(ft.Text('Copied to clipboard', size=15)))
        self.submission_form.page.set_clipboard(self.sql_statment)
        self.submission_form.rule_control.sql_result.value=f"""
```sql  
{self.sql_statment}  
```
"""
        self.page.update()
