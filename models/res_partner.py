from odoo import api, fields, models, api, exceptions
from datetime import datetime, timedelta,date
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class HrLiquidationgAccount(models.Model):
    _name = 'hr.liquidation.accounnt'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Account for account move"
    
    name = fields.Char('Referencia')
    account_1 = fields.Many2one('account.account')
    account_2 = fields.Many2one('account.account')
    account_3 = fields.Many2one('account.account')
    account_4 = fields.Many2one('account.account')
    account_5 = fields.Many2one('account.account')
    account_6 = fields.Many2one('account.account')
    account_7 = fields.Many2one('account.account')
    account_8 = fields.Many2one('account.account')
    account_9 = fields.Many2one('account.account')
    account_10 = fields.Many2one('account.account')
    account_11 = fields.Many2one('account.account')
    account_12 = fields.Many2one('account.account')
    account_13 = fields.Many2one('account.account')
    account_14 = fields.Many2one('account.account')
    account_15 = fields.Many2one('account.account')
    account_16 = fields.Many2one('account.account')
    account_17 = fields.Many2one('account.account')
    account_18 = fields.Many2one('account.account')
    account_19 = fields.Many2one('account.account')
    

#dd
class HrLiquidation(models.Model):
    _name = 'hr.liquidation.meca'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Liquidaciones"
    
    name = fields.Char("Referencia",store=True)
    days_wage = fields.Float("Días Laborados")
    last_wage = fields.Float("Anticipo Quincenal")
    extra_hours = fields.Float("Horas Extras")
    discounts = fields.Float("Prestamos/Descuentos")
    g_mov = fields.Float("Gastos de Movilización")
    employee_id = fields.Many2one("hr.employee","Empleado" , required=True)
    analytic_id = fields.Many2one("account.analytic.account","Analitica del Area" , required=True)
    account_move_close = fields.Many2one('account.move', string="Asiento Contable")
    last_date_b14 = fields.Date("Fecha Ultimo B.14", required=True)
    last_date_aguinaldo = fields.Date("Fecha de Ultimo Aguinaldo", required=True)
    amount_v10 = fields.Float("Pagos en v10") #HASTA QUE LLEGUE DICIEMBRE YA QUE NO HAY MAS PAYSLIP PARA PROMEDIO
    variable_bonus = fields.Float("Bono Variable")
    type = fields.Selection([
        ('1', 'Renuncia'),
        ('2', 'Despido'),],
        string='Motivo', required=True)
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('process', 'En Proceso'),
        ('done', 'Hecho'),],
        string='Estado',default='draft')
    
    amount_6 = fields.Float()
    amount_12 = fields.Float()
    
    title_type = fields.Char(default="TIPO")
    title_date_start = fields.Char(default="FECHA DE INGRESO")
    title_date_end = fields.Char(default="FECHA SALIDA")
    title_days = fields.Char(default="DÍAS")
    title_pay = fields.Char(default="PAGO")
    
    title_indem = fields.Char(default="INDEMNIZACION")
    title_aguinaldo = fields.Char(default="AGUINALDO")
    title_bono = fields.Char(default="BONO 14")
    title_vacaciones = fields.Char(default="VACACIONES")
    title_salario = fields.Char(default="SALARIO ")
    title_total = fields.Char(default="TOTAL ")
    title_ = fields.Char(default="- ")
    
    date_start = fields.Date()
    date_end = fields.Date()
    date_start_aguinaldo = fields.Date()
    date_start_b14 = fields.Date()
    date_start_salario = fields.Date()
    days_indemnizacion = fields.Float()
    days_aguinaldo = fields.Float()
    days_bono14 = fields.Float()
    days_vacaciones = fields.Float()
    days_salario = fields.Float()
    
    amount_indemnizacion = fields.Float()
    amount_aguinaldo = fields.Float()
    amount_b14 = fields.Float()
    amount_vacaciones = fields.Float()
    amount_salario = fields.Float()
    amount_salario_sbd = fields.Float()
    amount_total = fields.Float()
    amount_igss = fields.Float()
    amount_isr = fields.Float()
    amount_igss_pa = fields.Float()
    amount_extra_hours = fields.Float()
    amount_bf = fields.Float()
    amount_bd = fields.Float()
    amount_salary = fields.Float()
    amount_irtra = fields.Float()
    amount_acreedores = fields.Float()
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    acconunt_ids = fields.Many2one('hr.liquidation.accounnt', default=1)
    amount_duducciones = fields.Float()
    amount_devengado = fields.Float()
    data = fields.Html()
    #
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hr.liquidation')
        return super(HrLiquidation, self).create(vals)
    

    def amount_liquidation(self):

        date_start = self.employee_id.contract_id.date_start
        date_end = self.employee_id.contract_id.date_end
        difference_months = relativedelta(date_end, date_start)
        months = difference_months.years * 12 + difference_months.months
        
        self.date_start = date_start
        self.date_end = date_end
        self.date_start_aguinaldo = self.last_date_aguinaldo + timedelta(days=1)
        self.date_start_b14 = self.last_date_b14 + timedelta(days=1)
        #self.date_start_salario = self.last_day_pay + timedelta(days=1)
        
        #SEARCHS PARA LIQUIDACION CON SOLO 6 MESES
        limit_date = date_end - relativedelta(months=6) + timedelta(days=1)
        base_1q = sum(self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BASIC'),('slip_id.create_date', '>=',limit_date)]).mapped('total')) #SUMA DE SU INGRESO BASE PRIMERA QUINCENA
        base_2q = sum(self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BASE'),('slip_id.create_date', '>=',limit_date)]).mapped('total')) / 2 #SUMA DE SU INGRESO BASE SEGUNDA QUINCENA
        bofi_1q = sum(self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BONFIJAQ'),('slip_id.create_date', '>=',limit_date)]).mapped('total')) #SUMA DE SU INGRESO bonfijo primea QUINCENA
        bofi_2q = sum(self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BONFIJA'),('slip_id.create_date', '>=',limit_date)]).mapped('total')) / 2 #SUMA DE SU INGRESO bonfio SEGUNDA QUINCENA
        extra_hours = sum(self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'HorasS'),('slip_id.create_date', '>=',limit_date)]).mapped('total')) #SUMA DE SUS HORAS EXRAS
        
        
        #PARA MOSTRAR AL USUARIO DE DONDE SALEN LOS CALCULOS
        namepays = self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BASIC'),('slip_id.create_date', '>=',limit_date)]).mapped('slip_id.name')
        base_1q_dta = self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BASIC'),('slip_id.create_date', '>=',limit_date)]).mapped('total') #SUMA DE SU INGRESO BASE PRIMERA QUINCENA
        base_2q_dta = self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BASE'),('slip_id.create_date', '>=',limit_date)]).mapped('total') #SUMA DE SU INGRESO BASE SEGUNDA QUINCENA
        bofi_1q_dta = self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BONFIJAQ'),('slip_id.create_date', '>=',limit_date)]).mapped('total') #SUMA DE SU INGRESO bonfijo primea QUINCENA
        bofi_2q_dta = self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BONFIJA'),('slip_id.create_date', '>=',limit_date)]).mapped('total') #SUMA DE SU INGRESO bonfio SEGUNDA QUINCENA
        extra_hours_dta = self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'HorasS'),('slip_id.create_date', '>=',limit_date)]).mapped('total') #SUMA DE SUS HORAS EXRAS


        
        #SEARCHS PARA B14 Y AGUINALDO CON 12 MESES DE ANTIGUEDADd
        limit_date_12 = date_end - relativedelta(months=12) + timedelta(days=1)
        base_1q_12 = sum(self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BASIC'),('slip_id.create_date', '>=',limit_date_12)]).mapped('total')) #SUMA DE SU INGRESO BASE PRIMERA QUINCENA
        base_2q_12 = sum(self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BASE'),('slip_id.create_date', '>=',limit_date_12)]).mapped('total')) / 2#SUMA DE SU INGRESO BASE SEGUNDA QUINCENA
        bofi_1q_12 = sum(self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BONFIJAQ'),('slip_id.create_date', '>=',limit_date_12)]).mapped('total')) #SUMA DE SU INGRESO bonfijo primea QUINCENA
        bofi_2q_12 = sum(self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BONFIJA'),('slip_id.create_date', '>=',limit_date_12)]).mapped('total')) / 2#SUMA DE SU INGRESO bonfio SEGUNDA QUINCENA
        extra_hours_12 = sum(self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'HorasS'),('slip_id.create_date', '>=',limit_date_12)]).mapped('total')) #SUMA DE SUS HORAS EXRAS
        
        #PARA MOSTRAR AL USUARIO DE DONDE SALEN LOS CALCULOS
        payslips = self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BONFIJA'),('slip_id.create_date', '>=',limit_date_12)]).mapped('slip_id.name') #SUMA DE SU INGRESO BASE PRIMERA QUINCENA
        base_1q_12_dta = self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BASIC'),('slip_id.create_date', '>=',limit_date_12)]).mapped('total') #SUMA DE SU INGRESO BASE PRIMERA QUINCENA
        base_2q_12_dta = self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BASE'),('slip_id.create_date', '>=',limit_date_12)]).mapped('total')#SUMA DE SU INGRESO BASE SEGUNDA QUINCENA
        bofi_1q_12_dta = self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BONFIJAQ'),('slip_id.create_date', '>=',limit_date_12)]).mapped('total') #SUMA DE SU INGRESO bonfijo primea QUINCENA
        bofi_2q_12_dta = self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'BONFIJA'),('slip_id.create_date', '>=',limit_date_12)]).mapped('total')#SUMA DE SU INGRESO bonfio SEGUNDA QUINCENA
        extra_hours_12_dta = self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'HorasS'),('slip_id.create_date', '>=',limit_date_12)]).mapped('total') #SUMA DE SUS HORAS EXRAS

        
        self.data = f"<h3>Fecha inicial para promedio 6 meses: {limit_date}</h3> <p>Lotes a tomar: {namepays}</p> <p>Monto base 1Q: {base_1q_dta}</p><p>Monto base 2Q: {base_2q_dta}</p> <p>Monto BF 1Q: {bofi_1q_dta}</p> <p>Monto BF 2Q: {bofi_2q_dta}</p> <p>Monto H.E.: {extra_hours_dta}</p> <h3>Fecha inicial para promedio 12 meses: {limit_date_12}</h3> <p>Lotes a tomar: {payslips}</p> <p>Monto base 1Q: {base_1q_12_dta}</p><p>Monto base 2Q: {base_2q_12_dta}</p> <p>Monto BF 1Q: {bofi_1q_12_dta}</p> <p>Monto BF 2Q: {bofi_2q_12_dta}</p> <p>Monto H.E.: {extra_hours_12_dta}</p>"
        
        
        #SEARCH DEL ISR EN EL AÑO ACTUAL
        #actually_year = datetime.now().year
        #date_year = datetime(actually_year, 1, 1)
        #isr = sum(self.env['hr.payslip.line'].search([('employee_id', '=', self.employee_id.id),('code', '=', 'ISR'),('create_date', '>=',date_year.date())]).mapped('total')) #SUMA DE SUS HORAS EXRAS
        #self.amount_isr  = abs(round(isr,2))


        #CANTIDAD DE AÑOS PARA PAGAR INDEMNIZACION
        difference = date_end - date_start
        days = difference.days
        years = days / 365
        self.days_indemnizacion = days
        
        
        #CANTIDAD DE DIAS PARA PAGAR B14
        last_date_b14 =  date_end - self.last_date_b14
        difference_b14 = last_date_b14.days
        self.days_bono14 = difference_b14
        
        
        #CANTIDAD DE DIAS PARA PAGAR AGUINALDO
        last_date_aguinaldo = date_end - self.last_date_aguinaldo
        difference_aguinaldo = last_date_aguinaldo.days
        self.days_aguinaldo = difference_aguinaldo
        
        self.days_vacaciones = self.employee_id.vac
        
        if self.type == "1":
            #IF PARA EMPLEADO CON MENOS DE 12 MESES EN CONTRATO
            if months < 12:
                prom_ingre_12 = (base_1q_12 + base_2q_12 + bofi_1q_12 + bofi_2q_12 + extra_hours_12 + self.amount_v10) / days
                prom_month = round(prom_ingre_12 * 30,2)
                self.amount_12 = round(prom_month,2)

                
                #BONO 14
                self.amount_b14 = round((prom_month / 365) * difference_b14 ,2)
                #AGUINALDO
                self.amount_aguinaldo = round((prom_month / 365) * difference_aguinaldo ,2)
                #VACACIONES
                self.amount_vacaciones = round((prom_month / 30) * self.employee_id.vac ,2)

                #INDEMNIZACIONn
                self.amount_indemnizacion = 0.00
            else:
                prom_ingre_12 = (base_1q_12 + base_2q_12 + bofi_1q_12 + bofi_2q_12 +  extra_hours_12 + self.amount_v10) / 12
                self.amount_12 = round(prom_ingre_12,2)
                #INDEMNIZACION
                self.amount_indemnizacion = 0.00
                #BONO 14
                self.amount_b14 = round((prom_ingre_12 / 365) * difference_b14 ,2)
                #AGUINALDO
                self.amount_aguinaldo = round((prom_ingre_12 / 365) * difference_aguinaldo ,2)
                #VACACIONES
                self.amount_vacaciones = round((prom_ingre_12 / 30) * self.employee_id.vac ,2)
        else:
            #IF PARA EMPLEADO CON MENOS DE 12 MESES EN CONTRATO
            if months < 12:
                prom_ingre_12 = (base_1q_12 + base_2q_12 + bofi_1q_12 + bofi_2q_12 + extra_hours_12 + self.amount_v10) / days
                prom_month = round(prom_ingre_12 * 30,2)
                self.amount_12 = round(prom_month,2)
                #BONO 14
                self.amount_b14 = round((prom_month / 365) * difference_b14 ,2)
                #AGUINALDO
                self.amount_aguinaldo = round((prom_month / 365) * difference_aguinaldo ,2)
                #VACACIONES
                self.amount_vacaciones = round((prom_month / 30) * self.employee_id.vac ,2)
                
                print("Eestoy en despido 12 meses")
                if months < 6:
                    b14_agui = (base_1q + base_2q + bofi_1q + bofi_2q + extra_hours)/12
                    prom_ingre = (base_1q + base_2q + bofi_1q + bofi_2q + b14_agui + b14_agui + extra_hours) / days
                    prom_month_6 = round(prom_ingre * 30 ,2)
                    self.amount_6 = round(prom_month_6,2)
                    print("estoy en 6 meses")
                    #INDEMNIZACION
                    self.amount_indemnizacion = round(prom_month_6 * years,2)
                else:
                    b14_agui = (base_1q + base_2q + bofi_1q + bofi_2q + extra_hours)/12
                    prom_ingre = (base_1q + base_2q + bofi_1q + bofi_2q + b14_agui + b14_agui + extra_hours) / 6
                    prom_month_6 = round(prom_ingre,2)
                    self.amount_6 = round(prom_month_6,2)
                    print("estoy en mas de 6 meses")
                    #INDEMNIZACION
                    self.amount_indemnizacion = round(prom_month_6 * years,2)
            else:
                prom_ingre_12 = (base_1q_12 + base_2q_12 + bofi_1q_12 + bofi_2q_12 + extra_hours_12 + self.amount_v10) / 12
                b14_agui = (base_1q + base_2q + bofi_1q + bofi_2q + extra_hours)/12
                prom_ingre = (base_1q + base_2q + bofi_1q + bofi_2q + b14_agui + b14_agui + extra_hours) / 6
                self.amount_6 = round(prom_ingre,2)
                self.amount_12 = round(prom_ingre_12,2)
                
                #INDEMNIZACION
                self.amount_indemnizacion = round(prom_ingre * years,2)
                #BONO 14
                self.amount_b14 = round((prom_ingre_12 / 365) * difference_b14 ,2)
                #AGUINALDO
                self.amount_aguinaldo = round((prom_ingre_12 / 365) * difference_aguinaldo ,2)
                #VACACIONES
                self.amount_vacaciones = round((prom_ingre_12 / 30) * self.employee_id.vac ,2)

        
        
        #wagee
        wage = self.employee_id.contract_id.wage
        day_wage = wage/30
        bono_decreto = self.employee_id.contract_id.bono_decreto
        bono_fijo = self.employee_id.contract_id.base_extra
        day_bf = bono_fijo / 30
        self.amount_salario = round(((wage + bono_decreto + bono_fijo)/30) * self.days_wage ,2)
        self.days_salario = self.days_wage
        self.amount_salario_sbd = round(((wage + bono_fijo)/30) * self.days_wage ,2)
        
        self.amount_bd = round((bono_decreto / 30) * self.days_wage,2)
        self.amount_bf = round((bono_fijo / 30) * self.days_wage,2)
        self.amount_salary = round((wage / 30) * self.days_wage,2)
        
        #HORAS EXTRAS
        amount_hours = round((((day_wage + day_bf) / 8)*1.5 )* self.extra_hours ,2)
        self.amount_extra_hours = amount_hours
        

        #IGSS A PAGAR
        igss = round(((day_wage * self.days_wage )+amount_hours)*0.0483 ,2)
        self.amount_igss = igss
        
        igss_patronal = round(((day_wage * self.days_wage )+amount_hours)*0.1067 ,2)
        self.amount_igss_pa = igss_patronal
        
        irtra_patronal = round(((day_wage * self.days_wage )+amount_hours)*0.01 ,2)
        self.amount_irtra = irtra_patronal
        
        self.amount_acreedores = round((self.amount_salary + self.amount_bf + self.amount_bd + self.amount_extra_hours + self.amount_indemnizacion 
                                  + self.amount_aguinaldo + self.amount_b14 + self.amount_vacaciones  + self.g_mov + self.amount_isr + self.variable_bonus)-(self.amount_igss + self.last_wage + self.discounts),2)
        
        self.amount_total = round((self.amount_indemnizacion + self.amount_aguinaldo + self.amount_b14 + self.amount_vacaciones + self.amount_salario + self.amount_isr + self.amount_extra_hours + self.g_mov + self.variable_bonus) - (self.amount_igss  + self.discounts + self.last_wage),2)
        
        self.amount_devengado = round((self.amount_indemnizacion + self.amount_aguinaldo + self.amount_b14 + self.amount_vacaciones + self.amount_salario + self.amount_isr + self.amount_extra_hours + self.g_mov+ self.variable_bonus),2)
        self.amount_duducciones = round((self.amount_igss  + self.discounts + self.last_wage),2)

    def process(self):
        self.state = 'process'
    
    def done(self):
        self.state = 'done'
        
        analytic_distribution = {str(self.analytic_id.id): 100}
        move_line_vals = []
        journal_id = 0
        partner_id = self.employee_id.address_home_id.id
        credit_account_id = 0
        debit_account_id = 0
        
        journal_id = self.env['account.journal'].search([('name', '=', "Nomina")], limit=1)
        account_1 = self.acconunt_ids.account_1.id 
        account_2 = self.acconunt_ids.account_2.id
        account_3 = self.acconunt_ids.account_3.id
        account_4 = self.acconunt_ids.account_4.id
        account_5 = self.acconunt_ids.account_5.id
        account_6 = self.acconunt_ids.account_6.id
        account_7 = self.acconunt_ids.account_7.id
        account_8 = self.acconunt_ids.account_8.id
        account_9 = self.acconunt_ids.account_9.id
        account_10 = self.acconunt_ids.account_10.id
        account_11 = self.acconunt_ids.account_11.id
        account_12 = self.acconunt_ids.account_12.id
        account_13 = self.acconunt_ids.account_13.id
        account_14 = self.acconunt_ids.account_14.id
        account_15 = self.acconunt_ids.account_15.id
        account_16 = self.acconunt_ids.account_16.id
        account_17 = self.acconunt_ids.account_17.id
        account_18 = self.acconunt_ids.account_18.id
        account_19 = self.acconunt_ids.account_19.id


        # Debito Sueldos
        move_line_vals.append((0, 0, {
            'name': 'Sueldos ' + self.employee_id.name,
            'debit': self.amount_salary,
            'account_id': account_1,
            'analytic_distribution': analytic_distribution,
        }))
        
        # Debito Bono decreto
        move_line_vals.append((0, 0, {
            'name': 'Bono Decreto ' + self.employee_id.name,
            'debit': self.amount_bd,
            'account_id': account_2,
            'analytic_distribution': analytic_distribution,
        }))
        
        # Debito Bono Fijo
        move_line_vals.append((0, 0, {
            'name': 'Bono Fijo ' + self.employee_id.name,
            'debit': self.amount_bf,
            'account_id': account_2,
            'analytic_distribution': analytic_distribution,
        }))
        
        # Debito Horas Extras
        move_line_vals.append((0, 0, {
            'name': 'Horas Extras ' + self.employee_id.name,
            'debit': self.amount_extra_hours,
            'account_id': account_3,
            'analytic_distribution': analytic_distribution,
        }))
        
        # Credito IGSS Laboral
        move_line_vals.append((0, 0, {
            'name': 'IGSS Laboral ' + self.employee_id.name,
            'credit': self.amount_igss,
            'account_id': account_4,
            #'analytic_distribution': analytic_distribution,
        }))
        
        # Debito IGSS Patronal
        move_line_vals.append((0, 0, {
            'name': 'IGSS Patronal ' + self.employee_id.name,
            'debit': self.amount_igss_pa,
            'account_id': account_5,
            'analytic_distribution': analytic_distribution,
        }))
        
        # Credito IGSS Laboral por pagar
        move_line_vals.append((0, 0, {
            'name': 'IGSS por pagar ' + self.employee_id.name,
            'credit': self.amount_igss_pa,
            'account_id': account_6,
            #'analytic_distribution': analytic_distribution,
        }))
        
        # Debito Irtra Patronal
        move_line_vals.append((0, 0, {
            'name': 'Irtra Patronal ' + self.employee_id.name,
            'debit': self.amount_irtra,
            'account_id': account_7,
            'analytic_distribution': analytic_distribution,
        }))
        
        # Credito Irtra Laboral por pagar
        move_line_vals.append((0, 0, {
            'name': 'Irtra por pagar ' + self.employee_id.name,
            'credit': self.amount_irtra,
            'account_id': account_8,
            #'analytic_distribution': analytic_distribution,
        }))
        
        # Debito Intecap Patronal
        move_line_vals.append((0, 0, {
            'name': 'Intecap Patronal ' + self.employee_id.name,
            'debit': self.amount_irtra,
            'account_id': account_9,
            'analytic_distribution': analytic_distribution,
        }))
        
        # Credito Intecap Laboral por pagar
        move_line_vals.append((0, 0, {
            'name': 'Intecap por pagar ' + self.employee_id.name,
            'credit': self.amount_irtra,
            'account_id': account_10,
            #'analytic_distribution': analytic_distribution,
        }))
        
        # Debito INDEMNIZACION
        move_line_vals.append((0, 0, {
            'name': 'Indemnizacion ' + self.employee_id.name,
            'debit': self.amount_indemnizacion,
            'account_id': account_11,
            #'analytic_distribution': analytic_distribution,
        }))

        # Debito AGUINALDO
        move_line_vals.append((0, 0, {
            'name': 'AGUINALO ' + self.employee_id.name,
            'debit': self.amount_aguinaldo,
            'account_id': account_12,
            #'analytic_distribution': analytic_distribution,
        }))
        
        # Debito B14
        move_line_vals.append((0, 0, {
            'name': 'BONO 14 ' + self.employee_id.name,
            'debit': self.amount_b14,
            'account_id': account_13,
            #'analytic_distribution': analytic_distribution,
        }))

        # Debito BONO VARIABLE
        move_line_vals.append((0, 0, {
            'name': 'BONO VARIABLE ' + self.employee_id.name,
            'debit': self.variable_bonus,
            'account_id': account_19,
            #'analytic_distribution': analytic_distribution,
        }))
        
        # Debito VACA
        move_line_vals.append((0, 0, {
            'name': 'VACACIONES ' + self.employee_id.name,
            'debit': self.amount_vacaciones,
            'account_id': account_14,
            'analytic_distribution': analytic_distribution,
        }))
        
        # Debito gastos mov
        move_line_vals.append((0, 0, {
            'name': 'Gastos de Movilizacion ' + self.employee_id.name,
            'debit': self.g_mov,
            'account_id': account_15,
            'analytic_distribution': analytic_distribution,
        }))
        
        # Credito anticipo salarial
        move_line_vals.append((0, 0, {
            'name': 'Anticipo Salarial' + self.employee_id.name,
            'credit': self.last_wage,
            'account_id': account_16,
            #'analytic_distribution': analytic_distribution,
        }))
        
        # Credito otros descuentos
        move_line_vals.append((0, 0, {
            'name': 'Otros Descuentos' + self.employee_id.name,
            'credit': self.discounts,
            'account_id': account_16,
            #'analytic_distribution': analytic_distribution,
        }))
        
        # Debito ISR
        move_line_vals.append((0, 0, {
            'name': 'DEV ISR ' + self.employee_id.name,
            'debit': self.amount_isr,
            'account_id': account_17,
            #'analytic_distribution': analytic_distribution,
        }))
        
        #CREDITO ACREEDORES
        move_line_vals.append((0, 0, {
            'name': 'ACREEDORES ' + self.employee_id.name,
            'credit': self.amount_acreedores,
            'account_id': account_18,
            'partner_id': partner_id,
            #'analytic_distribution': analytic_distribution,
        }))

        # Asiento
        account_move = self.env['account.move'].create({
            'ref': 'Liquidacion de ' + self.employee_id.name,
            'date': date.today(),
            'journal_id': journal_id.id,
            'line_ids': move_line_vals,
        })
        
        self.account_move_close = account_move.id