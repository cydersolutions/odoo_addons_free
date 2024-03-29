# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Cs_car_poolCs_car_pool(models.Model):
    _name = "cs_car_pool.cs_car_pool"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Cs_car_pool"
    _order = "date_start desc, date_end desc, od_start desc, od_end desc"

    ref = fields.Char(string='Ref Number', default='New', tracking=True)
    name = fields.Many2one('hr.employee', "Driver", required=True, tracking=True)
    # name = fields.Many2one('res.user', "Driver", default=lambda self: self.env.user, required=True, tracking=True)
    date_start = fields.Datetime(string='Start Date', default=lambda self: fields.Datetime.now(), required=True, tracking=True)
    date_end = fields.Datetime(string='End Date', default=lambda self: fields.Datetime.now(), required=True, tracking=True)
    vehicle_id = fields.Many2one('cs_car_pool.vehicles', 'Vehicle', required=True, tracking=True)
    trip_purpose = fields.Char(string='Purpose', required=True, tracking=True)
    od_start = fields.Integer(string='Start Odometer', required=True, tracking=True)
    od_end = fields.Integer(string='End Odometer', required=True, tracking=True)
    trip_business = fields.Boolean(string='Business', default=True, tracking=True)
    distance = fields.Integer(string="Distance", compute="_compute_business_distance")


    @api.depends('od_start','od_end')
    def _compute_business_distance(self):
        for rec in self:
            rec.distance = rec.od_end - rec.od_start

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('cs_car_pool_log.sequence')
        # self.car_pool.veh_last_reading = self.od_end
        if vals['od_end'] < vals['od_start']:
            raise ValidationError(_("Ending odometer reading cannot be lower than the starting odometer reading"))
        return super(Cs_car_poolCs_car_pool, self).create(vals)

    def write(self, vals):
        if 'od_end' in vals:
            if vals['od_end'] < self.od_start:
                raise ValidationError(_("Ending odometer reading cannot be lower than the starting odometer reading"))
            if 'od_start' in vals:
                if vals['od_end'] < vals['od_start']:
                    raise ValidationError(
                        _("Ending odometer reading cannot be lower than the starting odometer reading"))
        return super(Cs_car_poolCs_car_pool, self).write(vals)

    @api.onchange('vehicle_id')
    def update_car_pool(self):
        for rec in self:
            rec.od_start = rec.vehicle_id.veh_last_reading

    @api.onchange('name')
    def update_pref_car_pool(self):
        for rec in self:
            rec.vehicle_id = rec.name.preferred_vehicle
            # rec.vehicle_id = rec.name.employee_id.preferred_vehicle

    @api.onchange('od_end')
    def update_od_end(self):
        for rec in self:
            if rec.od_end == 0:
                rec.od_end = rec.vehicle_id.veh_last_reading
            else:
                if rec.od_end >= rec.od_start:
                    rec.vehicle_id.veh_last_reading = rec.od_end
                else:
                    rec.od_end = rec.vehicle_id.veh_last_reading
                    raise ValidationError(_("Error: End odometer cannot be lower than the start"))

    @api.onchange('od_start')
    def update_od_start(self):
        for rec in self:
            if rec.od_start < rec.vehicle_id.veh_last_reading:
                rec.od_start = rec.vehicle_id.veh_last_reading
                raise ValidationError(_("Start odometer reading cannot be lower than the previous trip readings"))

    def set_end_to_now(self):
        self.date_end = fields.Datetime.now()

    @api.onchange('trip_business')
    def private_use(self):
        for rec in self:
            if rec.trip_business:
                if rec.trip_purpose == "Private Use":
                    rec.trip_purpose = ""
            else:
                rec.trip_purpose = "Private Use"