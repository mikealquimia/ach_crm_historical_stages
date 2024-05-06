# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    historical_stage_ids = fields.One2many('historical.stage.crm','lead_id', string="Historical Stage")

    @api.onchange('stage_id')
    def _onchange_stage_historical(self):
        for rec in self:
            if len(self.env['historical.stage.crm'].search([('lead_id','=',rec._origin.id),('stage_id','=',rec.stage_id.id),('date','=',date.today())])) == 0:
                historical_stage_id = self.env['historical.stage.crm'].create({'lead_id':rec._origin.id, 'stage_id':rec.stage_id.id,'date':date.today()})

    def write(self, vals):
        res = super(CrmLead, self).write(vals)
        if 'stage_id' in vals:
            for rec in self:
                if len(self.env['historical.stage.crm'].search([('lead_id','=',rec._origin.id),('stage_id','=',rec.stage_id.id),('date','=',date.today())])) == 0:
                    historical_stage_id = self.env['historical.stage.crm'].create({'lead_id':rec._origin.id, 'stage_id':rec.stage_id.id,'date':date.today()})
        return res

class HistoricalStageCrm(models.Model):
        _name = 'historical.stage.crm'
        _description = "Historical Stage CRM"

        lead_id = fields.Many2one('crm.lead', string="Opportunity")
        stage_id = fields.Many2one('crm.stage', string="Stage")
        date = fields.Date(string="Date")