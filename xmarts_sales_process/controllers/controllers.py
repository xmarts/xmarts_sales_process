# -*- coding: utf-8 -*-
from odoo import http

# class XmartsSalesProcess(http.Controller):
#     @http.route('/xmarts_sales_process/xmarts_sales_process/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/xmarts_sales_process/xmarts_sales_process/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('xmarts_sales_process.listing', {
#             'root': '/xmarts_sales_process/xmarts_sales_process',
#             'objects': http.request.env['xmarts_sales_process.xmarts_sales_process'].search([]),
#         })

#     @http.route('/xmarts_sales_process/xmarts_sales_process/objects/<model("xmarts_sales_process.xmarts_sales_process"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('xmarts_sales_process.object', {
#             'object': obj
#         })