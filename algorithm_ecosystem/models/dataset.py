import base64

from odoo import models, fields, api, _


class AlgoEcoDataset(models.Model):
    _name = "dataset"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    dataset_file = fields.Binary(string="Dataset File", required=True, attachment=True)
    dataset_path = fields.Char(string="Dataset Path", required=True)
    filename = fields.Char(string="Filename", required=True)

    @api.model
    def create(self, vals):
        filename = (
            vals.get("name")
            .lower()
            .replace(" ", "_")
            .replace(".", "_")
            .replace("-", "_")
            + ".csv"
        )

        vals.update(
            {
                "filename": filename,
                "dataset_path": "algorithm_ecosystem/datasets/" + filename,
            }
        )
        vals.update({"filename": filename})
        res = super(AlgoEcoDataset, self).create(vals)
        with open(res.dataset_path, "wb") as file:
            file.write(base64.b64decode(res.dataset_file))
        return res
