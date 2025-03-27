import flet as ft


class RuleControl(ft.Column):
    def __init__(self):
        super().__init__()
        self.rule_id=ft.Dropdown(options=self.get_rule_options(), label="rule_id", on_change=self.rule_dropdown_changed, value="R0001")
        self.sub_account=ft.Dropdown(options=self.get_sub_account_options(), label="sub_account", width=200, value='SA01')
        self.amount=ft.TextField(label="amount", value=100, input_filter=ft.InputFilter(regex_string=r"^(\d+(\.\d*)?|\.\d+)$", allow=True))
        self.number_of_days=ft.TextField(label="number_of_days", value=10, input_filter=ft.NumbersOnlyInputFilter())
        self.times=ft.TextField(label="times",value=1,input_filter=ft.NumbersOnlyInputFilter(),keyboard_type=ft.KeyboardType.NUMBER,)
        self.controls = [
            self.rule_id,
            self.sub_account,
            self.amount,
            self.number_of_days,
            self.times,
        ]
    
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
                self.sub_account.visible = False
                self.amount.visible = False
                self.number_of_days.visible = False
                self.times.visible = False
            case 'R0002'|'R0003':
                self.sub_account.visible = True
                self.amount.visible = False
                self.number_of_days.visible = True
                self.times.visible = False
            case 'R0004':
                self.sub_account.visible = True
                self.amount.visible = True
                self.number_of_days.visible = False
                self.times.visible = False
            case 'R0005':
                self.sub_account.visible = True
                self.amount.visible = True
                self.number_of_days.visible = True
                self.times.visible = False
            case 'R0006':
                self.sub_account.visible = True
                self.amount.visible = True
                self.number_of_days.visible = True
                self.times.visible = True
            case 'R0007':
                self.sub_account.visible = True
                self.amount.visible = True
                self.number_of_days.visible = False
                self.times.visible = True
            case 'R0008':
                self.sub_account.visible = False
                self.amount.visible = True
                self.number_of_days.visible = False
                self.times.visible = False
            case 'R0009':
                self.sub_account.visible = False
                self.amount.visible = True
                self.number_of_days.visible = False
                self.times.visible = True
        self.page.update()

    def get_sub_account_options(self):
        options = []
        options.append( ft.DropdownOption( key='SA01', content=ft.Text(value='SA01'), ) )
        options.append( ft.DropdownOption( key='SA02', content=ft.Text(value='SA02'), ) )
        options.append( ft.DropdownOption( key='SA03', content=ft.Text(value='SA03'), ) )
        options.append( ft.DropdownOption( key='SA04', content=ft.Text(value='SA04'), ) )
        options.append( ft.DropdownOption( key='SA05', content=ft.Text(value='SA05'), ) )
        return options
    
    def did_mount(self):
        self.rule_dropdown_changed(ft.ControlEvent(target=self.rule_id,
            name="change",
            data=self.rule_id.value,
            control=self.rule_id,
            page=self.page))