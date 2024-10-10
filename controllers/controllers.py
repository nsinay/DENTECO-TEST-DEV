# -*- coding: utf-8 -*-
# from odoo import http


# class TestDevDenteco(http.Controller):
#     @http.route('/test_dev_denteco/test_dev_denteco', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_dev_denteco/test_dev_denteco/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_dev_denteco.listing', {
#             'root': '/test_dev_denteco/test_dev_denteco',
#             'objects': http.request.env['test_dev_denteco.test_dev_denteco'].search([]),
#         })

#     @http.route('/test_dev_denteco/test_dev_denteco/objects/<model("test_dev_denteco.test_dev_denteco"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_dev_denteco.object', {
#             'object': obj
#         })
