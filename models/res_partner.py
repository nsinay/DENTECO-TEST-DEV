from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    custom_external = fields.Boolean(string="Custom External", default=False)
    studio_field = fields.Char(string="Campo Odoo Studio")