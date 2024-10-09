# -*- coding: utf-8 -*-
{
    'name': "Gestión de Proyectos MECA",

    'summary': """
        Desarrollo personalizado Para Meca Empresarial, S.A.""",

    'description': """
        Desarrollo personalizado Para Meca Empresarial, S.A.
    """,

    'author': "Jorge Marroquin",
    'website': "http://www.meca.com.gt",
    'license': 'LGPL-3',

    'category': 'Localization',
    'version': '16.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'hr','contacts'],

    # always loaded
    'data': [
        'data/data.xml',
        

        'security/ir.model.access.csv',
        'views/hr_liquidation_views.xml',
        'views/infraestructure_inventory_views.xml',

        'reports/report_action.xml',
        'reports/hr_liquidation_report.xml',
        'reports/report_infraestructure_inventory.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        
    ],
}
