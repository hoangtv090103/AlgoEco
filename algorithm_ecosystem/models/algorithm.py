from odoo import models, fields, api, _
import base64


class AlgoEcoAlgorithm(models.Model):
    _name = "algorithm"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    source_code = fields.Binary(string="Source Code", required=True, attachment=True)
    filename = fields.Char(string="Filename", required=True)
    script_path = fields.Char(string="Script Path", required=True)

    @api.model
    def create(self, vals):
        filename = (
            vals.get("name")
            .lower()
            .replace(" ", "_")
            .replace(".", "_")
            .replace("-", "_")
            + ".py"
        )
        vals.update(
            {
                "filename": filename,
                "script_path": "algorithm_ecosystem/algorithms/" + filename,
            }
        )
        res = super(AlgoEcoAlgorithm, self).create(vals)
        with open(res.script_path, "wb") as file:
            file.write(base64.b64decode(res.source_code))
        return res
