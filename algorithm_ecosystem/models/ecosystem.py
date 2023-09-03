import base64
import csv
import importlib.util
import io

from odoo import models, fields


class AlgoEcoEcosystem(models.Model):
    _name = "ecosystem"
    _rec_name = "display_name"

    display_name = fields.Char(compute='_compute_display_name', store=True)
    algorithm_id = fields.Many2one("algorithm", string="Algorithm", required=True, help="Algorithm to be used")
    dataset_id = fields.Many2one("dataset", string="Dataset", required=True, help="Dataset to be used")
    accuracy = fields.Char(string="Accuracy", readonly=True, help="Accuracy of the algorithm with the dataset")
    line_ids = fields.One2many("ecosystem.line", "ecosystem_id", string="Lines")

    def _compute_display_name(self):
        for record in self:
            record.display_name = record.algorithm_id.name + " - " + record.dataset_id.name

    def _get_class_name(self):
        script = io.StringIO(
            base64.b64decode(self.algorithm_id.source_code).decode("utf-8")
        )
        class_name = ""
        for line in script:
            if "class" in line:
                class_name = (
                    line.split(" ")[1].split("(")[0].replace(":", "").replace("\n", "")
                )
                break
        return class_name

    def get_module(self):
        module_name = self.algorithm_id.filename.split(".")[0]
        location = self.algorithm_id.script_path
        spec = importlib.util.spec_from_file_location(
            module_name, location
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return getattr(module, self._get_class_name())

    def action_run_ecosystem(self):
        for record in self:
            file = open(record.dataset_id.dataset_path, "r")

            dataset = csv.reader(file)
            class_name = self._get_class_name()
            spec = importlib.util.spec_from_file_location(
                class_name, record.algorithm_id.script_path
            )

            algorithm_obj = record.get_module()
            algorithm_obj = algorithm_obj(dataset, 3)

            test_len = len(algorithm_obj.test_labels)

            record.line_ids = [(2, id) for id in record.line_ids.ids]
            for i in range(test_len):
                record.line_ids = [
                    (
                        0,
                        0,
                        {
                            "test_label": algorithm_obj.test_labels[i],
                            "pred_label": algorithm_obj.pred_labels[i],
                            "is_correct": algorithm_obj.test_labels[i]
                            == algorithm_obj.pred_labels[i],
                        },
                    )
                ]
            record.accuracy = str(round(algorithm_obj.accuracy * 100, 2)) + "%"
            return True


class AlgoEcoEcosystemLine(models.Model):
    _name = "ecosystem.line"

    ecosystem_id = fields.Many2one("ecosystem", string="Ecosystem")
    test_label = fields.Char(string="Test Label")
    pred_label = fields.Char(string="Predicted Label")
    is_correct = fields.Boolean(string="Is Correct")
