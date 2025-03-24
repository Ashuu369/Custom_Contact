from . import custom_contact

# from .import request
import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import dateutil.parser
from datetime import datetime
from dateutil.parser import parse as date_parse


# from odoo.exceptions import ValidationError


class CustomContact(models.Model):
    _name = "custom.contact"
    _description = "Custom Contact with basic two fields"

    image = fields.Image(string="Image", required=True)
    name = fields.Char(string="Name", required=False)
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
        ],
        required=True,
    )
    designation = fields.Char(string="Designation")
    phone = fields.Char(string="Phone", required=False)
    address = fields.Char(string="Address", required=False)
    dob = fields.Date(string="Date of Birth", required=False, options = {'datepicker':{'maxDate':'fields.Date.today()'}})
    age = fields.Integer(string = "Age")
    email = fields.Char(string="Email")

    @api.constrains("phone")
    def _check_phone(self):
        for record in self:
            if record.phone:
                match = re.match("^[0-9]{10}$", record.phone)
                if not match:
                    raise ValidationError(_("Invalid phone number."))

    @api.constrains("name")
    def _check_name(self):
        for record in self:
            if record.name:
                # match = re.match('/^[a-zA-Z]+ [a-zA-Z]+$/', record.name)
                match = re.match(r"^[a-z A-Z]+$", record.name)
                # match = re.match('^[A-Za-z]{3,16})([ ]{0,1})([A-Za-z]{3,16})?([ ]{0,1})?([A-Za-z]{3,16})?([ ]{0,1})?([A-Za-z]{3,16})', record.name)
                if not match:
                    raise ValidationError(_("Invalid name."))

    @api.constrains("email")
    def _check_mail(self):
        for record in self:
            if record.email:
                match = re.match(
                    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", record.email
                )
                if not match:
                    raise ValidationError(_("Invalid Email."))

    @api.constrains("email")
    def check_email_database(self):
        for record in self:
            if record.email:
                existing_email = self.search(
                    [("email", "==", record.email), ("id", "!=", record.id)], limit=1
                )
                if existing_email:
                    raise ValidationError(_("Email already Registered"))

    @api.constrains("phone")
    def check_phone_database(self):
        for record in self:
            if record.phone:
                existing_number = self.search(
                    [("phone", "=", record.phone), ("id", "!=", record.id)], limit=1
                )
                if existing_number:
                    raise ValidationError(_("Number Already Registered."))


    @api.onchange('dob')
    def onchange_getage_id(self):
     for rec in self:
         if rec.dob:
          dob_year = rec.dob.year
          current_year = datetime.now().year
          age = current_year - dob_year
          if 10 <= age <= 100:
              rec.age = age
          else:
              raise ValidationError(_("Please Enter DOB Greater Than 10 Year."))

   

# class CustomContact(models.Model):

#     _name = 'custom.contact'
#     _description = 'Custom Contact with basic two fields'

#     name = fields.Char(string="name",required=True)
#     phone = fields.Char(string="phone",required=True)
#     address =  fields.Char(string = "address",required=True)
#     dob = fields.Date(string="dob", required=True, help="Date of Birth")
#     email = fields.Char(string = "email")

#     if re.match("^[0-9]\d{10}$", phone) == None:
#              raise ValidationError("Enter valid 10 digits Mobile number")
#     else:
#            None


# @api.onchange('phone')
# def validate_phone(self):
#  if self.phone:
#     match = re.match('^[0-9]\d{10}$', self.phone)
#     if not match:
#        raise ValidationError('Invalid')
#     elif match:
#        None
#     else:
#        None

# def validate_not_mobile(value):

#  rule = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$) ')

#  if rule.search(value):
#     msg = u"You cannot add mobile numbers."
#     raise ValidationError(msg)

# validate_not_mobile(phone)
# validate_phone(phone)
# class ResPartnerInherited(models.Model):
#     _inherit = "res.partner"

#     phone = fields.Char(max_length=10, string="Phone", required=True)

#     @api.constrains('phone')
#     def validate_phone(self):
#         for record in self:
#             if record.phone:
#                 match = re.match('^[6-9]\d{9}$', record.phone)
#                 if not match:
#                     raise ValidationError(_('Invalid phone number. Please enter a valid 10-digit Indian phone number.'))

#     @api.model
#     def create(self, vals):
#         if vals.get('phone'):
#             existing = self.search([('phone', '=', vals['phone'])], limit=1)
#             if existing:
#                 raise ValidationError(_("Another user is already using it ."))
#         return super(ResPartnerInherited, self).create(vals)