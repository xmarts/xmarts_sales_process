# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions,_

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    no_validate_sale = fields.Boolean(string='Sin validación de venta')
    is_carrier = fields.Boolean(string='Es transportista')

    @api.onchange('supplier')
    def onchange_supplier_tr(self):
        if self.supplier == False:
            self.is_carrier = False

class TransporterRoutes(models.Model):
    _name = 'sales.route'

    name = fields.Char(string='Nombre de la ruta')
    origin = fields.Char(string='Origen')
    destination = fields.Char(string='Destino')
    time = fields.Float(string='Tiempo aproximado de entrega (Horas).')

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    #Datos generales en el pedido
    valid_from = fields.Date(string='Vigente desde')
    valid_until = fields.Date(string='Vigente hasta')
    publication_date = fields.Date(string='Fecha de publicación')
    rev_cred_coll = fields.Boolean(string='Validado por credito y cobranza', default=False)
    rev_logistic = fields.Boolean(string='Validado por logistica', default=False)

    #Datos en nueva sección
    deadline = fields.Datetime(string='Fecha/Hora de entrega')
    confirmation_number = fields.Char(string='Nº de confirmación')
    observations = fields.Text(string='Observaciones')
    carrier_line = fields.Many2one('res.partner', string='Linea de transportista')
    operator_name = fields.Char(string='Nombre del operador')
    license_number = fields.Char(string='Nº de licencia')
    license_type = fields.Selection([
        ('autom', 'Automovilista'),
        ('chofer', 'Chofer'),
        ('federal', 'Federal')], string='Tipo de licencia')
    route = fields.Many2one('sales.route',string='Ruta')
    clean_unit = fields.Boolean(string='Unidad limpia', default=False)
    no_leaks = fields.Boolean(string='Sin filtraciones de luz o agua', default=False)
    damage_door_floor = fields.Boolean(string='Daños en pisos o puertas', default=False)
    odor_free = fields.Boolean(string='Libre de olores', default=False)
    no_graffiti = fields.Boolean(string='No graffiti', default=False)
    empty_weight = fields.Integer(string='Peso vacio (Kg)')
    loaded_weight = fields.Integer(string='Peso cargado (Kg)')
    transport_observations = fields.Text(string='Observaciones del transporte')
    transport_state = fields.Selection([
        ('accepted','Aceptado'),
        ('rejected','Rechazado'),
        ('in_route','En ruta'),
        ('delivered','Entregado')], string='Estado del transporte')

    @api.multi
    def action_confirm(self):
        self.ensure_one()
        res = super(SaleOrder, self).action_confirm()
        if self.partner_id.no_validate_sale == False:
            if self.rev_cred_coll == True and self.rev_logistic == True:
                return res
            else:
                if self.rev_cred_coll == True and self.rev_logistic == False:
                    raise exceptions.ValidationError('El pedido aun tiene que ser validado por logistica')
                if self.rev_cred_coll == False and self.rev_logistic == True:
                    raise exceptions.ValidationError('El pedido aun tiene que ser validado por credito y cobranza')
                if self.rev_cred_coll == False and self.rev_logistic == False:
                    raise exceptions.ValidationError('El pedido aun tiene que ser validado por credito y cobranza y logistica')
        else:
            return res

    @api.multi
    def action_cancel(self):
        self.rev_cred_coll = False
        self.rev_logistic = False
        res = super(SaleOrder, self).action_cancel()
        return res



# class xmarts_sales_process(models.Model):
#     _name = 'xmarts_sales_process.xmarts_sales_process'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100